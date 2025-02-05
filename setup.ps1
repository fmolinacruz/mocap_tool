# Create main directory structure
New-Item -ItemType Directory -Force -Path "E:\QT\Tools\mocap_tool"
Set-Location "E:\QT\Tools\mocap_tool"

# Create project subdirectories
New-Item -ItemType Directory -Force -Path "src"
New-Item -ItemType Directory -Force -Path "src\data_handlers"
New-Item -ItemType Directory -Force -Path "src\visualization"
New-Item -ItemType Directory -Force -Path "tests"
New-Item -ItemType Directory -Force -Path ".vscode"

# Create Python virtual environment
python -m venv venv

# Activate virtual environment and install packages
& .\venv\Scripts\Activate.ps1
pip install PyQt6==6.8.0 pytest pytest-qt

# Create __init__.py files
New-Item -ItemType File -Force -Path "src\__init__.py"
New-Item -ItemType File -Force -Path "src\data_handlers\__init__.py"
New-Item -ItemType File -Force -Path "src\visualization\__init__.py"
New-Item -ItemType File -Force -Path "tests\__init__.py"

Write-Host "Project structure created successfully!"
