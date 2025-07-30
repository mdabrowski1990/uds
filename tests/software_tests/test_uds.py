import pytest

import uds


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

    def test_getattr(self):
        for name in uds.__all__:
            assert getattr(uds, name)

    # __dir__

    def test_dir(self):
        assert dir(uds) == sorted(uds.__all__)
