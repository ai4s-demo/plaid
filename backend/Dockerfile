FROM --platform=linux/amd64 public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /app

# Install MiniZinc bundle (includes Gecode solver)
# fzn-gecode requires libgl1, libegl1, libfontconfig1, libfreetype6, libgpg-error0 at runtime
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates \
       libgl1 libegl1 libfontconfig1 libfreetype6 libgpg-error0 \
    && curl -fsSL https://github.com/MiniZinc/MiniZincIDE/releases/download/2.8.5/MiniZincIDE-2.8.5-bundle-linux-x86_64.tgz \
       -o /tmp/minizinc.tgz \
    && tar xzf /tmp/minizinc.tgz -C /opt \
    && mv /opt/MiniZincIDE-2.8.5-bundle-linux-x86_64 /opt/minizinc \
    && rm /tmp/minizinc.tgz \
    && apt-get purge -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/minizinc/bin:${PATH}"
ENV LD_LIBRARY_PATH="/opt/minizinc/lib:${LD_LIBRARY_PATH}"
ENV MZN_STDLIB_DIR="/opt/minizinc/share/minizinc"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
