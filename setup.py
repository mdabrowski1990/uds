import setuptools
import re


with open("uds/__init__.py", "r", encoding="utf-8") as init_file:
    author = re.search(r'^__author__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    email = re.search(r'^__email__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    maintainer = re.search(r'^__maintainer__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)
    init_file.seek(0)
    license_type = re.search(r'^__license__\s*=\s*[\'"]([^\'"]*)[\'"]', init_file.read(), re.MULTILINE).group(1)

packages = setuptools.find_packages(exclude=["tests", "tests.*", "docs", "docs.*"])

setuptools.setup(author=author,
                 author_email=email,
                 maintainer=maintainer,
                 maintainer_email=email,
                 packages=packages,
                 license=license_type)
