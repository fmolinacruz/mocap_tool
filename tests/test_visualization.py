# tests/test_visualization.py
import sys
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.visualization.motion_visualizer import MotionVisualizer
from src.data_handlers.mvn_data_handler import MVNDataHandler, XSensConfig

@pytest.fixture
def app():
    """Create Qt Application instance for testing"""
    app = QApplication(sys.argv)
    yield app
    app.quit()

@pytest.fixture
def visualizer(app):
    """Create MotionVisualizer instance for testing"""
    return MotionVisualizer()

def test_visualizer_creation(visualizer):
    """Test that visualizer creates without errors"""
    assert visualizer is not None
    assert visualizer.scene is not None
    assert visualizer.view is not None

def test_data_update(visualizer):
    """Test visualizer handles data updates"""
    test_data = {
        'header': 1,
        'timestamp': 0.0,
        'payload': {
            'raw_data': b'test'
        }
    }
    visualizer.update_data(test_data)
    # Should not raise any exceptions

def test_mvn_handler():
    """Test MVN handler basic functionality"""
    config = XSensConfig(
        host="localhost",
        port=9763
    )
    handler = MVNDataHandler(config)
    assert handler.config.host == "localhost"
    assert handler.config.port == 9763
    assert not handler.is_connected

def test_mvn_config():
    """Test MVN config handling"""
    config = XSensConfig(
        host="test_host",
        port=12345,
        protocol="TCP"
    )
    handler = MVNDataHandler(config)
    status = handler.get_status()
    assert status["config"]["host"] == "test_host"
    assert status["config"]["port"] == 12345
    assert status["config"]["protocol"] == "TCP"

if __name__ == "__main__":
    pytest.main(['-v', __file__])
