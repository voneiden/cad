cam = (
    JobV2(
        top=rotary_enc_coupler.faces('>Z').workplane().plane,
        feed=300,
        tool_diameter=1.0,
        plunge_feed=100)
    .profile(rotary_enc_coupler.faces('<Z'), inner_offset=-1, stepdown=1)
    .profile(rotary_enc_coupler.faces('<Z[1]'), outer_offset=-1, stepdown=1)
    .profile(rotary_enc_coupler.faces('<Z'), outer_offset=1, stepdown=1)
)


cam.save_gcode('pushpull.nc')
show_object(rotary_enc_coupler)
cam.show(show_object)
