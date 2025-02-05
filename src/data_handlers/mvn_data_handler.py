# src/data_handlers/mvn_data_handler.py
import socket
import struct
from dataclasses import dataclass
from typing import Optional, List, Dict, Tuple, Callable
import threading
import time
import json

@dataclass
class XSensConfig:
    """Configuration class for XSens MVN connection settings"""
    host: str = "localhost"      # Host address for MVN connection
    port: int = 9763            # Default MVN port
    protocol: str = "UDP"       # Connection protocol (UDP/TCP)
    buffer_size: int = 4096     # Size of receive buffer
    timeout: float = 1.0        # Socket timeout in seconds

class MVNDataHandler:
    """Handles communication with XSens MVN software"""
    def __init__(self, config: XSensConfig = None):
        self.config = config or XSensConfig()
        self.socket: Optional[socket.socket] = None
        self.is_connected = False
        self.is_streaming = False
        self._stop_streaming = False
        self.stream_thread: Optional[threading.Thread] = None
        self.data_callbacks: List[Callable] = []
        self._latest_data = None
        self.connection_status_callback: Optional[Callable] = None

    def set_connection_callback(self, callback: Callable[[bool, str], None]):
        self.connection_status_callback = callback

    def add_data_callback(self, callback: Callable):
        self.data_callbacks.append(callback)

    def connect(self) -> Tuple[bool, str]:
        try:
            if self.config.protocol == "UDP":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.socket.settimeout(self.config.timeout)
                self.socket.bind((self.config.host, self.config.port))
            else:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(self.config.timeout)
                self.socket.connect((self.config.host, self.config.port))
            
            self.is_connected = True
            if self.connection_status_callback:
                self.connection_status_callback(True, "Connected successfully")
            return True, "Connected successfully"
        except socket.error as e:
            error_msg = f"Failed to connect: {str(e)}"
            if self.connection_status_callback:
                self.connection_status_callback(False, error_msg)
            return False, error_msg

    def disconnect(self) -> Tuple[bool, str]:
        try:
            self.stop_streaming()
            if self.socket:
                self.socket.close()
                self.socket = None
            
            self.is_connected = False
            if self.connection_status_callback:
                self.connection_status_callback(False, "Disconnected")
            return True, "Disconnected successfully"
        except Exception as e:
            error_msg = f"Error during disconnect: {str(e)}"
            if self.connection_status_callback:
                self.connection_status_callback(False, error_msg)
            return False, error_msg

    def start_streaming(self) -> bool:
        if not self.is_connected:
            return False
            
        self.is_streaming = True
        self._stop_streaming = False
        self.stream_thread = threading.Thread(target=self._stream_data)
        self.stream_thread.daemon = True
        self.stream_thread.start()
        return True

    def stop_streaming(self):
        self._stop_streaming = True
        self.is_streaming = False
        if self.stream_thread:
            self.stream_thread.join(timeout=2.0)
            self.stream_thread = None

    def _stream_data(self):
        while not self._stop_streaming and self.socket:
            try:
                data = self._receive_packet()
                if data:
                    self._latest_data = data
                    for callback in self.data_callbacks:
                        callback(data)
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error in data stream: {e}")
                break

    def _receive_packet(self) -> Optional[Dict]:
        try:
            if self.config.protocol == "UDP":
                data, _ = self.socket.recvfrom(self.config.buffer_size)
            else:
                data = self.socket.recv(self.config.buffer_size)
                
            if not data:
                return None
                
            return self._parse_mvn_packet(data)
        except socket.timeout:
            return None
        except Exception as e:
            print(f"Error receiving packet: {e}")
            return None

    def _parse_mvn_packet(self, data: bytes) -> Optional[Dict]:
        try:
            if len(data) < 4:
                return None
                
            header = struct.unpack("!I", data[:4])[0]
            payload = data[4:]
            
            return {
                "header": header,
                "timestamp": time.time(),
                "data_size": len(payload),
                "payload": self._parse_payload(payload)
            }
        except Exception as e:
            print(f"Error parsing packet: {e}")
            return None

    def _parse_payload(self, payload: bytes) -> Dict:
        return {
            "raw_size": len(payload),
            "raw_data": payload
        }

    def get_latest_data(self) -> Optional[Dict]:
        return self._latest_data

    def get_status(self) -> Dict:
        return {
            "connected": self.is_connected,
            "streaming": self.is_streaming,
            "config": {
                "host": self.config.host,
                "port": self.config.port,
                "protocol": self.config.protocol
            }
        }
