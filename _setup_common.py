import fnmatch
import os
import sys

# required since Python 2.7's glob.iglob does not support recursive keyword
def recursive_glob(startpath, filepattern):
    """Return a list of files matching a pattern, searching recursively from a start path.

    Keyword Arguments:
    startpath -- starting path (directory)
    filepattern -- fnmatch-style filename pattern
    """
    return [
        os.path.join(dirpath, filename)
        for dirpath, _, filenames in os.walk(startpath)
        for filename in filenames
        if fnmatch.fnmatch(filename, filepattern)
    ]


open3 = open
if sys.version_info < (3, 0):
    import io

    open3 = io.open

# loosely from https://packaging.python.org/guides/single-sourcing-package-version/
HERE = os.path.abspath(os.path.dirname(__file__))

name = "pyaedt"

with open(os.path.join(HERE, "pyaedt", "version.txt"), "r") as f:
    version = f.readline()

author = "ANSYS, Inc."

maintainer = "Massimo Capodiferro"

maintainer_email = "massimo.capodiferro@ansys.com"

description = "Higher-Level Pythonic Ansys Electronics Desktop Framework"

# Get the long description from the README file
with open3(os.path.join(HERE, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

packages = [
    "pyaedt",
    "pyaedt.misc",
    "pyaedt.application",
    "pyaedt.modeler",
    "pyaedt.modules",
    "pyaedt.generic",
    "pyaedt.edb_core",
    "pyaedt.edb_core.edb_data",
    "pyaedt.emit_core",
    "pyaedt.examples",
    "pyaedt.rpc",
    "pyaedt.edb_core.ipc2581",
    "pyaedt.edb_core.ipc2581.bom",
    "pyaedt.edb_core.ipc2581.content",
    "pyaedt.edb_core.ipc2581.ecad",
    "pyaedt.edb_core.ipc2581.ecad.cad_data",
]

data_files = [
    ("dlls", recursive_glob(os.path.join("pyaedt", "dlls"), "*")),
    ("misc", recursive_glob(os.path.join("pyaedt", "misc"), "*")),
    ("License", recursive_glob(".", "*.md")),
    ("xaml", ["pyaedt/generic/wpf_template.xaml"]),
    ("version", ["pyaedt/version.txt"]),
    ("setup-distutils", ["setup-distutils.py"]),
]

license = "MIT"

classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
]

project_urls={
    "Bug Tracker": "https://github.com/pyansys/pyaedt/issues",
    "Documentation": "https://aedt.docs.pyansys.com",
    "Source Code": "https://github.com/pyansys/pyaedt",
}
