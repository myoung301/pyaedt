"""
SBR+: Import Geometry from Maps
-------------------------------
This example shows how you can use PyAEDT to create an HFSS SBR+ project from an
OpenStreeMaps.
"""
###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perrform rquired imports and set up the local path to the path for the PyAEDT
# directory.

import os
from pyaedt import Hfss


###############################################################################
# Set non-graphical mode
# ~~~~~~~~~~~~~~~~~~~~~~
# Set non-graphical mode. ``"PYAEDT_NON_GRAPHICAL"`` is needed to generate
# documentation only.
# You can set ``non_graphical`` either to ``True`` or ``False``.

non_graphical = os.getenv("PYAEDT_NON_GRAPHICAL", "False").lower() in ("true", "1", "t")

###############################################################################
# Define designs
# ~~~~~~~~~~~~~~
# Define two designs, one source and one target, with each design connected to
# a different object.

app = Hfss(
    designname="Ansys",
    solution_type="SBR+",
    specified_version="2022.2",
    new_desktop_session=True,
    non_graphical=non_graphical
)

###############################################################################
# Define Location to import
# ~~~~~~~~~~~~~~~~~~~~~~~~~
# Define latitude and longitude to import.
ansys_home = [40.273726, -80.168269]




###############################################################################
# Generate map and import
# ~~~~~~~~~~~~~~~~~~~~~~~
# Assign boundaries.

app.modeler.import_from_openstreet_map(ansys_home,
                                       terrain_radius=250,
                                       road_step=3,
                                       plot_before_importing=False,
                                       import_in_aedt=True)




###############################################################################
# Plot model
# ~~~~~~~~~~
# Plot the model

app.plot(show=False, export_path=os.path.join(app.working_directory, "Source.jpg"), plot_air_objects=True)


###############################################################################
# Release AEDT
# ~~~~~~~~~~~~
# Release AEDT and close the example.

if os.name != "posix":
    app.release_desktop()
