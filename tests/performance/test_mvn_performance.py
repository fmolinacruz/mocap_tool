import pytest
from src.data_handlers.mvn_data_handler import MVNDataHandler, XSensConfig

@pytest.mark.performance
def test_packet_processing_performance(benchmark):
    handler = MVNDataHandler()
    test_data = b'\x00\x00\x00\x01test_payload'
    benchmark(handler._parse_mvn_packet, test_data)
