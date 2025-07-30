import pytest
from mock import patch, Mock

import uds

class TestUDS:

    # __version__

    def test_version(self):
        major_version, minor_version, patch_version = uds.__version__.split(".")
        assert major_version.isdecimal()
        assert minor_version.isdecimal()
        assert patch_version.isdecimal()

    # __getattr__

    def test_getattr(self):
        for name in uds.__all__:
            assert getattr(uds, name)

    # __dir__

    def test_dir(self):
        assert dir(uds) == sorted(uds.__all__)
