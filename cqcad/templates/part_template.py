import cadquery as cq
import cqparts
from cqparts.constraints import LockConstraint, Mate

class Box(cqparts.Part):
    def make(self):
        # A unit cube centered on 0,0,0
        return cq.Workplane('XY').box(1, 1, 1)

box1 = Box().make()

# Render the box with grey RGB and no transparency
show_object(box1, options={"rgba": (204, 204, 204, 0.0)})