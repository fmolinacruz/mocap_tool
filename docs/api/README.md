# Motion Capture Tool API Documentation

## Core Components

### XSensConfig
`python
class XSensConfig:
    '''Configuration class for XSens MVN connection settings.

    Attributes:
        host (str): Host address for MVN connection. Default: 'localhost'
        port (int): Network port for connection. Default: 9763
        protocol (str): Connection protocol ('UDP' or 'TCP'). Default: 'UDP'
        buffer_size (int): Size of receive buffer. Default: 4096
        timeout (float): Socket timeout in seconds. Default: 1.0
    '''
`python
class MVNDataHandler:
    '''Handles communication with XSens MVN software.

    Manages UDP/TCP connections, data streaming, and packet processing
    for motion capture data from XSens MVN system.

    Attributes:
        config (XSensConfig): Configuration settings for MVN connection
        is_connected (bool): Current connection status
        is_streaming (bool): Current streaming status
        _stop_streaming (bool): Internal flag to control streaming thread
        stream_thread (Thread): Background thread for data reception
        data_callbacks (List[Callable]): Registered data processing callbacks
        connection_status_callback (Callable): Status update callback

    Methods:
        connect() -> Tuple[bool, str]:
            Establishes connection to MVN software using configured settings.
            Returns: (success status, status message)

        disconnect() -> Tuple[bool, str]:
            Closes active connection and cleans up resources.
            Returns: (success status, status message)

        start_streaming() -> bool:
            Begins data reception in background thread.
            Returns: True if streaming started successfully

        stop_streaming():
            Stops data reception and cleans up streaming thread.

        add_data_callback(callback: Callable):
            Registers callback function for receiving motion data.
            Args: callback - Function to receive parsed MVN data packets

        set_connection_callback(callback: Callable[[bool, str], None]):
            Sets callback for connection status updates.
            Args: callback - Function receiving (is_connected, status_message)

        get_status() -> Dict:
            Returns current state of the handler.
            Returns: Dict with connection status and configuration
    '''
