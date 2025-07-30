from unittest.mock import MagicMock

import pytest
from mock import patch

import uds

SCRIPT_LOCATION = "uds"

class TestUDS:
    """Unit tests for uds.__init__.py"""

    # __version__

    def test_version(self):
        major_version, minor_version, patch_version = uds.__version__.split(".")
        assert major_version.isdecimal()
        assert minor_version.isdecimal()
        assert patch_version.isdecimal()

    # __author__ and __maintainer__

    def test_author_and_maintainer(self):
        assert isinstance(uds.__author__, str)
        assert isinstance(uds.__maintainer__, str)
        assert uds.__author__ == uds.__maintainer__

    # __credits__

    def test_credits(self):
        assert isinstance(uds.__credits__, list)
        assert all(isinstance(credit, str) for credit in uds.__credits__)

    # __email__

    def test_email(self):
        assert isinstance(uds.__email__, str)
        assert "@" in uds.__email__

    # __license__

    def test_license(self):
        assert isinstance(uds.__license__, str)

    # __getattr__

    @pytest.mark.parametrize("name", ["something_that_is_not_defined", "__version__"])
    @patch(f"{SCRIPT_LOCATION}.sys")
    @patch(f"{SCRIPT_LOCATION}.importlib")
    def test_getattr__attribute_error(self, mock_importlib, mock_sys, name):
        with pytest.raises(AttributeError):
            uds.__getattr__(name)
        mock_importlib.assert_not_called()
        mock_sys.assert_not_called()

    @pytest.mark.parametrize("name", filter(lambda name: name[:2] != "__" and name[-2:] != "__", uds.__all__))
    @patch(f"{SCRIPT_LOCATION}.sys")
    @patch(f"{SCRIPT_LOCATION}.importlib")
    def test_getattr__attribute_error(self, mock_importlib, mock_sys, name):
        assert uds.__getattr__(name) == mock_importlib.import_module.return_value
        mock_importlib.import_module.assert_called_once_with(f"uds.{name}")
        mock_sys.modules.__setitem__.assert_called_once_with(f"uds.{name}",
                                                             mock_importlib.import_module.return_value)

    # __dir__

    def test_dir(self):
        assert dir(uds) == sorted(uds.__all__)
