import os
from pyaedt import Hfss

project_path = r'C:\Users\dcrawfor\OneDrive - ANSYS, Inc\Documents\Jupyter\AEDT Examples\project'
design_name = "design1"

if not os.path.exists(project_path):
    os.makedirs(project_path)

proj_name = "slot_ant.aedt"
with Hfss(projectname=os.path.join(project_path, proj_name),
          designname=design_name,
          release_on_exit=True,
          student_version=True) as hfss:
    ###############################################################################
    # Define parameters
    # ~~~~~~~~~~~~~~~
    # Set parameters to microns:
    units = "um"
    hfss.modeler.model_units = units
    params = {"slot_length": 980, "slot_width": 100, "feed_length": 1000,
              "x_size": 2000, "y_size": 2000, "t_oxide": 10, "w_trace": 10,
              "feed_offset": 0, "feed_inset": 200, "t_metal": 2,
              "via_offset": 20}
    for k, v in params.items():
        hfss[k] = str(v) + units
    plane_origin = ["-x_size/2", "-y_size/2", 0]
    plane_xy = ["x_size", "y_size"]
    bottom_plane = hfss.modeler.primitives.create_rectangle(0, plane_origin,
                                                            plane_xy,
                                                            name="bottom_plane",
                                                            matname="copper")
    bottom_plane.translate([0, 0, "-t_oxide/2"])
    bottom_plane.color = "Orange"
    bottom_plane.transparency = 0.25
    bottom_plane.thicken_sheet("-t_metal")

    top_plane = bottom_plane.duplicate_along_line([0, 0, "t_oxide + t_metal"], name="top_plane")[0]

    slot = hfss.modeler.primitives.create_box(["-slot_length/2", "-slot_width/2", "t_oxide/2"],
                                              ["slot_length", "slot_width", "t_metal"],
                                              name="slot")
    top_plane = top_plane - slot  # Boolean subtract
    via_base_position = ["slot_length/2 + via_offset", "slot_width/2 + via_offset", "-t_oxide/2"]
    via1 = hfss.modeler.primitives.create_cylinder(cs_axis="Z",
                                                  position=via_base_position,
                                                  radius="4um", height="t_oxide",
                                                  name="via1", matname="copper")
    via1.color = "Orange"
    via2 = via1.duplicate_and_mirror([0,0,0], [1,0,0], name="via2")
    via3 = via2.duplicate_and_mirror([0,0,0], [0,1,0], name="via3")
    via4 = via1.duplicate_and_mirror([0,0,0], [0,1,0], name="via4")
    trace =
    #top_plane = hfss.modeler.primitives.create_rectangle(position=plane_origin, [x_size, y_size],
    #                                                        name="top_plane", mat_name="copper")


pass