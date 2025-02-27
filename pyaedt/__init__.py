# -*- coding: utf-8 -*-
import os

if os.name == "nt":
    os.environ["PYTHONMALLOC"] = "malloc"
os.environ["ANS_MESHER_PROC_DUMP_PREPOST_BEND_SM3"] = "1"
os.environ["ANSYSEM_FEATURE_SF6694_NON_GRAPHICAL_COMMAND_EXECUTION_ENABLE"] = "1"
os.environ["ANSYSEM_FEATURE_SF159726_SCRIPTOBJECT_ENABLE"] = "1"
os.environ["ANSYSEM_FEATURE_SF222134_CABLE_MODELING_ENHANCEMENTS_ENABLE"] = "1"
pyaedt_path = os.path.dirname(__file__)
__version__ = ""
if os.path.exists(os.path.join(pyaedt_path, "version.txt")):
    with open(os.path.join(pyaedt_path, "version.txt"), "r") as f:
        __version__ = f.read().strip()


from pyaedt.generic import constants
from pyaedt.generic.general_methods import _pythonver
from pyaedt.generic.general_methods import _retry_ntimes
from pyaedt.generic.general_methods import generate_unique_folder_name
from pyaedt.generic.general_methods import generate_unique_name
from pyaedt.generic.general_methods import generate_unique_project_name
from pyaedt.generic.general_methods import inside_desktop
from pyaedt.generic.general_methods import is_ironpython
from pyaedt.generic.general_methods import pyaedt_function_handler
from pyaedt.generic.general_methods import settings

from pyaedt.aedt_logger import pyaedt_logger  # isort:skip

try:
    from pyaedt.generic.design_types import Hfss3dLayout
except:
    from pyaedt.generic.design_types import Hfss3dLayout

from pyaedt.generic.design_types import Circuit
from pyaedt.generic.design_types import Desktop
from pyaedt.generic.design_types import Edb
from pyaedt.generic.design_types import Emit
from pyaedt.generic.design_types import Hfss
from pyaedt.generic.design_types import Icepak
from pyaedt.generic.design_types import Maxwell2d
from pyaedt.generic.design_types import Maxwell3d
from pyaedt.generic.design_types import MaxwellCircuit
from pyaedt.generic.design_types import Mechanical
from pyaedt.generic.design_types import Q2d
from pyaedt.generic.design_types import Q3d
from pyaedt.generic.design_types import Rmxprt
from pyaedt.generic.design_types import Simplorer
from pyaedt.generic.design_types import Siwave
from pyaedt.generic.design_types import TwinBuilder
from pyaedt.generic.design_types import get_pyaedt_app
