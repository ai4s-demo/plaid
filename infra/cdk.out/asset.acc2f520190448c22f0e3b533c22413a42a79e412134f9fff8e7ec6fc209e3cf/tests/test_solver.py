"""Tests for constraint solver."""
import pytest
from app.solver import ConstraintSolver
from app.models import (
    SourcePlate, SourceWell, DesignParameters,
    PlateType, Distribution, SolveStatus
)


@pytest.fixture
def sample_source_plate():
    """Create sample source plate for testing."""
    wells = [
        SourceWell(position=f"A{i:02d}", gene_symbol=f"Gene{i}", volume=100)
        for i in range(1, 11)
    ]
    return SourcePlate(barcode="TEST_PLATE", wells=wells)


@pytest.fixture
def default_params():
    """Create default design parameters."""
    return DesignParameters(
        plate_type=PlateType.PLATE_96,
        replicates=6,
        edge_empty_layers=1,
        distribution=Distribution.UNIFORM
    )


class TestConstraintSolver:
    """Test cases for ConstraintSolver."""
    
    def test_solver_initialization(self, default_params):
        """Test solver initializes correctly."""
        solver = ConstraintSolver(default_params)
        assert solver.rows == 8
        assert solver.cols == 12
        assert solver.edge == 1
        assert solver.available_wells == 60  # (8-2) * (12-2)
    
    def test_solve_simple_layout(self, sample_source_plate, default_params):
        """Test solving a simple layout."""
        solver = ConstraintSolver(default_params)
        result = solver.solve(
            genes=sample_source_plate.get_genes(),
            source_plate=sample_source_plate,
            timeout_seconds=10
        )
        
        assert result.status in [SolveStatus.SUCCESS, SolveStatus.PARTIAL]
        assert len(result.layouts) > 0
    
    def test_position_formatting(self, default_params):
        """Test well position formatting."""
        solver = ConstraintSolver(default_params)
        
        assert solver._format_position(0, 0) == "A01"
        assert solver._format_position(0, 9) == "A10"
        assert solver._format_position(7, 11) == "H12"
    
    def test_quadrant_interleaving(self, default_params):
        """Test quadrant interleaving for uniform distribution."""
        solver = ConstraintSolver(default_params)
        
        positions = [(r, c) for r in range(1, 7) for c in range(1, 11)]
        interleaved = solver._interleave_by_quadrant(positions)
        
        # Should have same number of positions
        assert len(interleaved) == len(positions)
        
        # First 4 positions should be from different quadrants
        quadrants = set()
        for r, c in interleaved[:4]:
            q = (0 if r < 4 else 2) + (0 if c < 6 else 1)
            quadrants.add(q)
        assert len(quadrants) == 4
    
    def test_edge_constraint(self, sample_source_plate, default_params):
        """Test edge empty constraint."""
        solver = ConstraintSolver(default_params)
        result = solver.solve(
            genes=sample_source_plate.get_genes(),
            source_plate=sample_source_plate,
            timeout_seconds=10
        )
        
        if result.layouts:
            layout = result.layouts[0]
            for well in layout.wells:
                # Edge wells should be empty
                if (well.row < 1 or well.row >= 7 or
                    well.col < 1 or well.col >= 11):
                    assert well.content_type.value == "empty"
    
    def test_384_plate(self, sample_source_plate):
        """Test with 384-well plate."""
        params = DesignParameters(
            plate_type=PlateType.PLATE_384,
            replicates=6,
            edge_empty_layers=1,
            distribution=Distribution.UNIFORM
        )
        
        solver = ConstraintSolver(params)
        assert solver.rows == 16
        assert solver.cols == 24
        
        result = solver.solve(
            genes=sample_source_plate.get_genes(),
            source_plate=sample_source_plate,
            timeout_seconds=10
        )
        
        assert result.status in [SolveStatus.SUCCESS, SolveStatus.PARTIAL]


class TestParameterExtraction:
    """Test parameter extraction from natural language."""
    
    def test_extract_plate_type(self):
        """Test plate type extraction."""
        from app.services import AgentService
        agent = AgentService()
        
        params = agent.extract_parameters("使用384孔板")
        assert params.plate_type == PlateType.PLATE_384
        
        params = agent.extract_parameters("96-well plate")
        assert params.plate_type == PlateType.PLATE_96
    
    def test_extract_replicates(self):
        """Test replicate count extraction."""
        from app.services import AgentService
        agent = AgentService()
        
        params = agent.extract_parameters("每个基因6个重复")
        assert params.replicates == 6
        
        params = agent.extract_parameters("3 replicates per gene")
        assert params.replicates == 3
    
    def test_extract_edge_empty(self):
        """Test edge empty extraction."""
        from app.services import AgentService
        agent = AgentService()
        
        params = agent.extract_parameters("外圈留空")
        assert params.edge_empty_layers == 1
        
        params = agent.extract_parameters("边缘空白2层")
        assert params.edge_empty_layers == 2
    
    def test_extract_distribution(self):
        """Test distribution extraction."""
        from app.services import AgentService
        agent = AgentService()
        
        params = agent.extract_parameters("随机分布")
        assert params.distribution == Distribution.RANDOM
        
        params = agent.extract_parameters("按列排布")
        assert params.distribution == Distribution.COLUMN


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
