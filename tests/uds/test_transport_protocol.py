# import pytest
# from mock import Mock, patch
#
# from uds.transport_interface import AbstractTPInterface
#
#
# class TestAbstractTPInterface:
#     """Tests for AbstractTPInterface class."""
#
#     def setup(self):
#         self.mock_tp_interface = Mock(spec=AbstractTPInterface)
#
#     @pytest.mark.parametrize("addressing", ["physical", "functional", "broadcast"])
#     @pytest.mark.parametrize("suppress_response", [True, False])
#     def test_start_tester_present(self, addressing, suppress_response):
#         assert AbstractTPInterface.start_tester_present(self=self.mock_tp_interface) is None
