import pytest
from dataclasses import dataclass

@pytest.fixture
def mock_mvn_data():
    return {
        'header': 1,
        'timestamp': 0.0,
        'payload': {
            'raw_data': b'test'
        }
    }
