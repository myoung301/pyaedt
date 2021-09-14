import os
from pyaedt import Hfss

project_path = r'C:\Users\dcrawfor\OneDrive - ANSYS, Inc\Documents\Jupyter\AEDT Examples\project'
design_name = "design1"
proj_name = "slot_ant.aedt"

# TODO: create_rectangle() and create_cylinder() have inconsistent call signatures.

if not os.path.exists(project_path):
    os.makedirs(project_path)

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
    params = {"slot_length": 980, "slot_width": 100, "feed_length": 600,
              "x_size": 2000, "y_size": 2000, "t_oxide": 10, "w_trace": 10,
              "feed_offset": 0, "feed_extend": 200, "t_metal": 2,
              "via_offset": 20}
    via_radius = "4um"  # This is not parameterized in HFSS.
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
    bottom_plane.transparency = 0.35
    bottom_plane.thicken_sheet("-t_metal")

    top_plane = bottom_plane.duplicate_along_line([0, 0, "t_oxide + t_metal"], name="top_plane")[0]

    slot = hfss.modeler.primitives.create_box(["-slot_length/2", "-slot_width/2", "t_oxide/2"],
                                              ["slot_length", "slot_width", "t_metal"],
                                              name="slot")
    top_plane = top_plane - slot  # Boolean subtract
    top_plane.transparency = 0.8
    via_base_position = ["slot_length/2 + via_offset", "slot_width/2 + via_offset", "-t_oxide/2"]
    via1 = hfss.modeler.primitives.create_cylinder(cs_axis="Z",
                                                  position=via_base_position,
                                                  radius=via_radius, height="t_oxide",
                                                  name="via1", matname="copper")
    via1.color = "Orange"
    via2 = via1.duplicate_and_mirror([0, 0, 0], [1, 0, 0], name="via2")
    via3 = via2.duplicate_and_mirror([0, 0, 0], [0, 1, 0], name="via3")
    via4 = via1.duplicate_and_mirror([0, 0, 0], [0, 1, 0], name="via4")
    feed_start_pos = ["feed_offset", "-feed_length", 0]
    feed_end_pos = ["feed_offset", "slot_width/2 + feed_extend + 8um", 0]
    trace = hfss.modeler.primitives.create_polyline([feed_start_pos, feed_end_pos],
                                                    name="trace",
                                                    matname="copper",
                                                    xsection_type='Rectangle',
                                                    xsection_width="w_trace",
                                                    xsection_height="t_metal")
    feed_short_pos = ["feed_offset", "slot_width/2 + feed_extend", "-t_oxide/2"]
    feed_short = hfss.modeler.primitives.create_cylinder(cs_axis="Z",
                                                         position=feed_short_pos,
                                                         radius=via_radius,
                                                         height="t_oxide",
                                                         name="feed_short",
                                                         matname="copper")
    trace = trace + feed_short  # hfss.modeler.unite([trace, feed_short])  # TODO: Use __add__ dunder method.
    trace.color = "Orange"
    hfss.create_wave_port_from_sheet()
   #  port = hfss.create_lumped_port_between_objects(trace.name, bottom_plane.name, hfss.AxisDir.YNeg, portname="p1", renorm=False)
    # port_face_id = hfss.modeler.primitives.get_faceid_from_position(feed_start_pos, obj_name="trace")
    # port_sheet = hfss.modeler.create_sheet_to_ground(trace.name, groundname=bottom_plane.name, axisdir=5)
    pass
