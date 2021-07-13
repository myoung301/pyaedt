# Setup paths for module imports
from pyaedt.modeler.PrimitivesEmit import EmitComponent
from .conftest import local_path, scratch_path

# Import required modules
from pyaedt import Emit
from pyaedt.generic.filesystem import Scratch
import gc
import os


class TestEmit:

    def setup_class(self):
        project_name = "SimplorerProject"
        design_name = "SimplorerDesign1"
        # set a scratch directory and the environment / test data
        with Scratch(scratch_path) as self.local_scratch:
            self.aedtapp = Emit()

    def teardown_class(self):
        assert self.aedtapp.close_project(self.aedtapp.project_name)
        self.local_scratch.remove()
        gc.collect()

    def test_objects(self):
        assert self.aedtapp.solution_type
        assert isinstance(self.aedtapp.existing_analysis_setups, list)
        assert isinstance(self.aedtapp.setup_names, list)
        assert self.aedtapp.modeler
        assert self.aedtapp.oanalysis is None

    def test_create_components(self):
        radio_name = self.aedtapp.modeler.components.create_component("New Radio", "TestRadio")
        assert radio_name == "TestRadio"
        radio = self.aedtapp.modeler.components[radio_name]
        assert isinstance(radio, EmitComponent)
        antenna_name = self.aedtapp.modeler.components.create_component("Antenna", "TestAntenna")
        assert antenna_name == "TestAntenna"
        antenna = self.aedtapp.modeler.components[antenna_name]
        assert isinstance(antenna, EmitComponent)
