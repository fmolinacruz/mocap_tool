# src/main.py
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                          QTabWidget, QLabel, QPushButton, QHBoxLayout,
                          QStatusBar, QLineEdit, QFormLayout, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSlot, QTimer
from data_handlers.mvn_data_handler import MVNDataHandler, XSensConfig
from visualization.motion_visualizer import MotionVisualizer
import sys
from typing import Dict, Optional

class DeviceConfigWidget(QWidget):
   """Widget for configuring device connection settings"""
   def __init__(self, config: Dict, parent=None):
       super().__init__(parent)
       layout = QFormLayout()
       
       self.host_input = QLineEdit(config.get('host', 'localhost'))
       self.port_input = QLineEdit(str(config.get('port', 9763)))
       self.protocol_input = QLineEdit(config.get('protocol', 'UDP'))
       
       layout.addRow("Host:", self.host_input)
       layout.addRow("Port:", self.port_input)
       layout.addRow("Protocol:", self.protocol_input)
       
       self.setLayout(layout)
       
   def get_config(self) -> XSensConfig:
       return XSensConfig(
           host=self.host_input.text(),
           port=int(self.port_input.text()),
           protocol=self.protocol_input.text()
       )

class DeviceWidget(QWidget):
   """Widget for controlling and displaying device status"""
   def __init__(self, device_name, parent=None):
       super().__init__(parent)
       self.device_name = device_name
       self.is_connected = False
       self.handler: Optional[MVNDataHandler] = None
       self.visualizer = None
       
       # Create main layout
       main_layout = QVBoxLayout()
       
       # Status and connect button layout
       control_layout = QHBoxLayout()
       self.status_label = QLabel(f"{device_name}: Disconnected")
       self.connect_button = QPushButton("Connect")
       self.connect_button.clicked.connect(self.toggle_connection)
       
       control_layout.addWidget(self.status_label)
       control_layout.addWidget(self.connect_button)
       
       # Add configuration widget if it's XSens
       if device_name == 'XSens':
           self.config_widget = DeviceConfigWidget({
               'host': 'localhost', 
               'port': 9763
           })
           main_layout.addWidget(self.config_widget)
       else:
           self.config_widget = None
           
       main_layout.addLayout(control_layout)
       self.setLayout(main_layout)

   def set_visualizer(self, visualizer: MotionVisualizer):
       self.visualizer = visualizer
       
   def connection_status_callback(self, connected: bool, message: str):
       self.is_connected = connected
       status = "Connected" if connected else "Disconnected"
       self.status_label.setText(f"{self.device_name}: {status}")
       self.connect_button.setText("Disconnect" if connected else "Connect")
       
       if message:
           QMessageBox.information(self, "Connection Status", message)
   
   def data_callback(self, data: Dict):
       if self.visualizer:
           self.visualizer.update_data(data)
   
   @pyqtSlot()
   def toggle_connection(self):
       if self.device_name == 'XSens':
           if not self.is_connected:
               if not self.handler:
                   self.handler = MVNDataHandler(self.config_widget.get_config())
                   self.handler.set_connection_callback(self.connection_status_callback)
                   self.handler.add_data_callback(self.data_callback)
               
               success, message = self.handler.connect()
               if success:
                   self.handler.start_streaming()
           else:
               if self.handler:
                   self.handler.disconnect()
                   self.handler = None

class MocapToolWindow(QMainWindow):
   """Main window for the Motion Capture Tool"""
   def __init__(self):
       super().__init__(None, Qt.WindowType.Window)
       self.setWindowTitle("Mocap Tool")
       
       # Create main widget and layout
       main_widget = QWidget()
       self.setCentralWidget(main_widget)
       layout = QVBoxLayout(main_widget)
       
       # Create tabs
       tabs = QTabWidget()
       
       # Devices tab
       devices_tab = QWidget()
       devices_layout = QVBoxLayout(devices_tab)
       devices_layout.addWidget(QLabel("Device Control"))
       
       self.device_widgets = {}
       for device in ['XSens', 'StretchSense', 'Live Link']:
           widget = DeviceWidget(device)
           self.device_widgets[device] = widget
           devices_layout.addWidget(widget)
       
       devices_layout.addStretch()
       tabs.addTab(devices_tab, "Devices")
       
       # Add Visualization tab
       visualization_tab = QWidget()
       visualization_layout = QVBoxLayout(visualization_tab)
       self.visualizer = MotionVisualizer()
       visualization_layout.addWidget(self.visualizer)
       tabs.addTab(visualization_tab, "Visualization")
       
       # Connect visualizer to XSens device
       if 'XSens' in self.device_widgets:
           self.device_widgets['XSens'].set_visualizer(self.visualizer)
       
       # Recording tab
       recording_tab = QWidget()
       recording_layout = QVBoxLayout(recording_tab)
       recording_layout.addWidget(QLabel("Recording Controls"))
       
       self.record_button = QPushButton("Start Recording")
       self.record_button.clicked.connect(self.toggle_recording)
       recording_layout.addWidget(self.record_button)
       
       self.recording_status = QLabel("Status: Ready")
       recording_layout.addWidget(self.recording_status)
       
       recording_layout.addStretch()
       tabs.addTab(recording_tab, "Recording")
       
       # Add tabs to main layout
       layout.addWidget(tabs)
       
       # Create status bar
       self.status_bar = QStatusBar()
       self.setStatusBar(self.status_bar)
       self.status_bar.showMessage("Ready")
       
       # Set window properties
       self.setMinimumSize(800, 600)
       self.is_recording = False

   def showEvent(self, event):
       """Handle window show event"""
       super().showEvent(event)
       QTimer.singleShot(100, self.activateWindow)
       QTimer.singleShot(100, self.raise_)
   
   @pyqtSlot()
   def toggle_recording(self):
       self.is_recording = not self.is_recording
       if self.is_recording:
           self.record_button.setText("Stop Recording")
           self.recording_status.setText("Status: Recording")
           self.status_bar.showMessage("Recording in progress...")
       else:
           self.record_button.setText("Start Recording")
           self.recording_status.setText("Status: Ready")
           self.status_bar.showMessage("Recording stopped")

def main():
   app = QApplication(sys.argv)
   window = MocapToolWindow()
   window.show()
   window.raise_()
   window.activateWindow()
   sys.exit(app.exec())

if __name__ == "__main__":
   main()
