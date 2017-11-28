import cadquery as cq

width = 10.0
height = 10.0
depth = 10.0

result = cq.Workplane('XY').box(width, height, depth)

# Render the model with grey RGB and no transparency
show_object(result, options={"rgba": (204, 204, 204, 0.0)})