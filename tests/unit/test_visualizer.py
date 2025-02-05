# tests/unit/test_visualizer.py
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPointF
from src.visualization.motion_visualizer import MotionScene, MotionVisualizer

@pytest.fixture(scope="module")
def qapp():
    """Create QApplication instance for all tests"""
    app = QApplication([])
    yield app
    app.quit()

class TestMotionScene:
    """Unit tests for MotionScene class"""
    
    @pytest.fixture
    def scene(self):
        """Create fresh MotionScene for each test"""
        return MotionScene()
    
    def test_initial_state(self, scene):
        """Test initial state of MotionScene"""
        assert len(scene.skeleton_points) == 0
        assert len(scene.motion_trail) == 0
        assert scene.max_trail_length == 50
    
    def test_update_skeleton(self, scene):
        """Test skeleton update functionality"""
        test_points = [
            QPointF(0, 0),
            QPointF(1, 1),
            QPointF(2, 2)
        ]
        
        scene.update_skeleton(test_points)
        assert len(scene.skeleton_points) == 3
        assert len(scene.motion_trail) == 1
        
        # Test trail length limit
        for _ in range(60):  # More than max_trail_length
            scene.update_skeleton(test_points)
        assert len(scene.motion_trail) == scene.max_trail_length

class TestMotionVisualizer:
    """Unit tests for MotionVisualizer class"""
    
    @pytest.fixture
    def visualizer(self, qapp):
        """Create fresh MotionVisualizer for each test"""
        return MotionVisualizer()
    
    def test_initial_state(self, visualizer):
        """Test initial state of MotionVisualizer"""
        assert visualizer.scene is not None
        assert visualizer.view is not None
        assert visualizer.info_label.text() == "No data"
    
    def test_data_update(self, visualizer):
        """Test data update handling"""
        test_data = {
            'header': 42,
            'timestamp': 123.456,
            'payload': {
                'raw_data': b'test'
            }
        }
        
        visualizer.update_data(test_data)
        assert visualizer.info_label.text() == "Frame: 42"

if __name__ == "__main__":
    pytest.main(['-v', __file__])
