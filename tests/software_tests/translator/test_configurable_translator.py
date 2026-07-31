import pytest
from mock import call, Mock, MagicMock, patch
from uds.translator.configurable_translator import ConfigurableTranslator, Translator

SCRIPT_LOCATION = "uds.translator.configurable_translator"


class TestConfigurableTranslator:
    """Unit tests for `ConfigurableTranslator` class."""

    def setup_method(self):
        self.mock_translator = MagicMock(spec=ConfigurableTranslator,
                                         __class__=ConfigurableTranslator)
        # patching
        self._patcher_deepcopy = patch(f"{SCRIPT_LOCATION}.deepcopy")
        self.mock_deepcopy = self._patcher_deepcopy.start()

    def teardown_method(self):
        self._patcher_deepcopy.stop()

    # __init__

    @pytest.mark.parametrize("services", [
        [Mock()],
        [Mock(), Mock()],
    ])
    @patch(f"{SCRIPT_LOCATION}.Translator.__init__")
    def test_init__mandatory_args(self, mock_translator_init, services):
        mock_base = Mock(spec=Translator, services=services)
        assert ConfigurableTranslator.__init__(self.mock_translator, mock_base) is None
        self.mock_translator._ConfigurableTranslator__adapt_subfunction.assert_not_called()
        self.mock_deepcopy.assert_has_calls([call(service) for service in services], any_order=True)
        mock_translator_init.assert_called_once()
