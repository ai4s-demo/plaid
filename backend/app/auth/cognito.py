"""Cognito JWT verification."""
import json
import httpx
from typing import Optional
from functools import lru_cache
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.config import settings


class CognitoUser(BaseModel):
    """Authenticated user from Cognito."""
    sub: str  # Cognito user ID
    username: str
    email: Optional[str] = None
    name: Optional[str] = None


# HTTP Bearer scheme
security = HTTPBearer(auto_error=False)


@lru_cache()
def get_cognito_public_keys() -> dict:
    """Fetch and cache Cognito public keys (JWKS)."""
    if not settings.cognito_user_pool_id:
        return {}
    
    region = settings.cognito_region
    pool_id = settings.cognito_user_pool_id
    
    jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/jwks.json"
    
    try:
        response = httpx.get(jwks_url, timeout=10)
        response.raise_for_status()
        jwks = response.json()
        
        # Convert to dict keyed by kid
        keys = {}
        for key in jwks.get("keys", []):
            keys[key["kid"]] = key
        return keys
    except Exception as e:
        print(f"Failed to fetch Cognito JWKS: {e}")
        return {}


def verify_token(token: str) -> CognitoUser:
    """Verify Cognito JWT token and extract user info."""
    
    if not settings.cognito_user_pool_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication not configured"
        )
    
    try:
        # Get the key ID from token header
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        
        if not kid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token header"
            )
        
        # Get public keys
        keys = get_cognito_public_keys()
        key = keys.get(kid)
        
        if not key:
            # Refresh keys cache and try again
            get_cognito_public_keys.cache_clear()
            keys = get_cognito_public_keys()
            key = keys.get(kid)
            
            if not key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unable to find appropriate key"
                )
        
        # Verify token
        region = settings.cognito_region
        pool_id = settings.cognito_user_pool_id
        client_id = settings.cognito_app_client_id
        
        issuer = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}"
        
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=client_id,
            issuer=issuer,
            options={"verify_at_hash": False}
        )
        
        # Extract user info
        return CognitoUser(
            sub=payload.get("sub", ""),
            username=payload.get("cognito:username", payload.get("username", "")),
            email=payload.get("email"),
            name=payload.get("name"),
        )
        
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[CognitoUser]:
    """
    Get current authenticated user.
    
    Returns None if auth is not configured or no token provided.
    Raises HTTPException if token is invalid.
    """
    # If auth is not configured, allow anonymous access
    if not settings.cognito_user_pool_id:
        return None
    
    # If no credentials provided
    if not credentials:
        return None
    
    return verify_token(credentials.credentials)


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> CognitoUser:
    """
    Require authentication.
    
    Use this dependency for endpoints that require authentication.
    """
    if not settings.cognito_user_pool_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication not configured"
        )
    
    return verify_token(credentials.credentials)
