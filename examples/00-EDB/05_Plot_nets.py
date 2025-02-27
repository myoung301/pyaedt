"""
EDB: plot nets with Matplotlib
------------------------------
This example shows how you can use the ``Edb`` class to plot a net or a layout.
"""

###############################################################################
# Perform required imports
# ~~~~~~~~~~~~~~~~~~~~~~~~
# Perform required imports, which includes importing a section.

import os
from pyaedt import generate_unique_folder_name, examples, Edb

###############################################################################
# Download file
# ~~~~~~~~~~~~~
# Download the AEDT file and copy it into the temporary folder.

temp_folder = generate_unique_folder_name()

targetfolder = os.path.dirname(examples.download_aedb(temp_folder))


###############################################################################
# Launch EDB
# ~~~~~~~~~~
# Launch the :class:`pyaedt.Edb` class, using EDB 2022 R2 and SI units.

edb = Edb(edbpath=targetfolder, edbversion="2022.2")

###############################################################################
# Plot custom set of nets colored by layer
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot a custom set of nets colored by layer (default).

edb.core_nets.plot("V3P3_S0")

###############################################################################
# Plot custom set of nets colored by nets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot a custom set of nets colored by nets.

edb.core_nets.plot(["VREF", "V3P3_S0"], color_by_net=True)

###############################################################################
# Plot all nets on a layer colored by nets
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Plot all nets on a layer colored by nets

edb.core_nets.plot(None, ["TOP"], color_by_net=True, plot_components_on_top=True)

###############################################################################
# Close EDB
# ~~~~~~~~~
# Close EDB.

edb.close_edb()
