# Motion Capture Tool

A Python-based motion capture tool for managing and visualizing data from multiple capture devices.

## Features
- XSens MVN integration
- Real-time motion visualization
- Recording capabilities
- Multi-device support

## Setup
1. Clone the repository
2. Create virtual environment:
   `powershell
   python -m venv venv
   .\venv\Scripts\activate
   `
3. Install dependencies:
   `powershell
   pip install -r requirements.txt
   `

## Configuration
To ensure the buffer size is correctly set, use the following assertion:
```python
buffer_size = 1024  # Update this value to the correct expected value
print(f"Expected buffer size: {buffer_size}")
print(f"Actual buffer size: {config.buffer_size}")
assert config.buffer_size == buffer_size, f"Buffer size should be {buffer_size}"
```
# Testing Strategy

## Testing Levels

### Unit Testing (White Box)
#### Individual component testing
#### Focus on code coverage and edge cases
#### Mock external dependencies

### Integration Testing (Gray Box)
#### Component interaction testing
#### Focus on data flow and state management
#### Partial mocking of external systems

### System Testing (Black Box)
#### End-to-end functionality testing
#### User scenario validation
#### Real system integration
