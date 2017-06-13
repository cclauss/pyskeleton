import ast
import importlib
import os
from setuptools import setup, find_packages

import pip
from pkg_resources import safe_name

PKG_DIR = 'package'


def find_version():
    """Return value of __version__.

    Reference: https://stackoverflow.com/a/42269185/
    """
    file_path = importlib.util.find_spec(PKG_DIR).origin
    with open(file_path) as file_obj:
        root_node = ast.parse(file_obj.read())
    for node in ast.walk(root_node):
        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and node.targets[0].id == "__version__":
                return node.value.s
    raise RuntimeError("Unable to find version string.")


def parse_requirements():
    """Return requirements from requirements.txt.

    The "MANIFEST.in" file must exist with the line "include requirements.txt".

    This implementation is tested to be compatible with pip 9.0.1.

    Reference: https://stackoverflow.com/q/14399534/
    """
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = list(pip.req.parse_requirements(requirements_path, session=pip.download.PipSession()))
    install_requires = [str(r.req) for r in requirements]
    return install_requires


setup(
    name=safe_name(PKG_DIR),
    version=find_version(),
    packages=find_packages(include=[PKG_DIR, PKG_DIR + '.*']),
    install_requires=parse_requirements(),
)
