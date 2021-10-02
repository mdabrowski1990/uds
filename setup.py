import setuptools
import re

install_requires = [
    "aenum"
]

with open("uds/__init__.py", "r", encoding="utf-8") as init_file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    email = re.search(r'^__email__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    maintainer = re.search(r'^__maintainer__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    license_type = re.search(r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)

packages = setuptools.find_packages(exclude=["tests", "tests.*", "docs", "docs.*"])

setuptools.setup(version=version,
                 author=author,
                 author_email=email,
                 maintainer=maintainer,
                 packages=packages,
                 license=license_type,
                 install_requires=install_requires)
