# tests/unit/test_mvn_handler.py

# Importing the pytest module for writing test cases
import pytest

# Importing the MVNDataHandler and XSensConfig classes from the src.data_handlers.mvn_data_handler module
from src.data_handlers.mvn_data_handler import MVNDataHandler, XSensConfig

# Defining a test class for XSensConfig
class TestXSensConfig:
    """Unit tests for XSensConfig class"""
    
    # Test method to check the default configuration of XSensConfig
    def test_default_config(self):
        """Test that default configuration is set correctly"""
        # Creating an instance of XSensConfig with default values
        config = XSensConfig()
        
        # Asserting that the default host is "localhost"
        assert config.host == "localhost"
        
        # Asserting that the default port is 9763
        assert config.port == 9763
        
        # Asserting that the default protocol is "UDP"
        assert config.protocol == "UDP"
        
        # Asserting that the default buffer size is 4096
        assert config.buffer_size == 4096
        
        # Asserting that the default timeout is 1.0 seconds
        assert config.timeout == 1.0
    
    # Test method to check the custom configuration of XSensConfig
    def test_custom_config(self):
        """Test that custom configuration values are set correctly"""
        # Creating an instance of XSensConfig with custom values
        config = XSensConfig(
            host="test_host",  # Custom host value
            port=12345,        # Custom port value
            protocol="TCP",    # Custom protocol value
            buffer_size=8192,  # Custom buffer size value
            timeout=2.0        # Custom timeout value
        )
        
        # Asserting that the custom host is set correctly
        assert config.host == "test_host"
        
        # Asserting that the custom port is set correctly
        assert config.port == 12345
        
        # Asserting that the custom protocol is set correctly
        assert config.protocol == "TCP"
        
        # Asserting that the custom buffer size is set correctly
        assert config.buffer_size == 8192
        
        # Asserting that the custom timeout is set correctly
        assert config.timeout == 2.0

# Defining a test class for MVNDataHandler
class TestMVNDataHandler:
    """Unit tests for MVNDataHandler class"""
    
    # Defining a pytest fixture to create a fresh MVNDataHandler instance for each test
    @pytest.fixture
    def handler(self):
        """Create a fresh MVNDataHandler instance for each test"""
        return MVNDataHandler()
    
    # Test method to check the initial state of MVNDataHandler
    def test_initial_state(self, handler: MVNDataHandler):
        """Test initial state of MVNDataHandler"""
        # Asserting that the handler is not connected initially
        assert not handler.is_connected
        
        # Asserting that the handler is not streaming initially
        assert not handler.is_streaming
        
        # Asserting that the _stop_streaming attribute is False initially
        assert handler._stop_streaming == False
        
        # Asserting that the stream_thread attribute is None initially
        assert handler.stream_thread is None
        
        # Asserting that the data_callbacks list is empty initially
        assert len(handler.data_callbacks) == 0
        
        # Asserting that the _latest_data attribute is None initially
        assert handler._latest_data is None
        
        # Asserting that the connection_status_callback attribute is None initially
        assert handler.connection_status_callback is None
    
    # Test method to check the callback registration functions
    def test_callback_registration(self, handler: MVNDataHandler):
        """Test callback registration functions"""
        # Defining a dummy callback function
        def dummy_callback(*args):
            pass
            
        # Test connection callback
        handler.set_connection_callback(dummy_callback)
        
        # Asserting that the connection_status_callback is set correctly
        assert handler.connection_status_callback == dummy_callback
        
        # Test data callback
        handler.add_data_callback(dummy_callback)
        
        # Asserting that the data_callbacks list has one callback
        assert len(handler.data_callbacks) == 1
        
        # Asserting that the data_callbacks list contains the dummy callback
        assert handler.data_callbacks[0] == dummy_callback
    
    # Test method to check the MVN packet parsing
    def test_packet_parsing(self, handler: MVNDataHandler):
        """Test MVN packet parsing"""
        # Creating dummy packet data
        dummy_data = b'\x00\x00\x00\x01test_payload'
        
        # Parsing the dummy packet data
        parsed = handler._parse_mvn_packet(dummy_data)
        
        # Asserting that the parsed data is not None
        assert parsed is not None
        
        # Asserting that the header is parsed correctly
        assert parsed['header'] == 1
        
        # Asserting that the timestamp is present in the parsed data
        assert 'timestamp' in parsed
        
        # Asserting that the data_size is parsed correctly
        assert parsed['data_size'] == len(b'test_payload')
        
        # Asserting that the raw_size of the payload is parsed correctly
        assert parsed['payload']['raw_size'] == len(b'test_payload')

# Running the tests if the script is executed directly
if __name__ == "__main__":
    pytest.main(['-v', __file__])
