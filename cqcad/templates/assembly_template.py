import cadquery as cq
from cqparts import Assembly, Part
from cqparts.constraints import LockConstraint, Mate

class Box(Part):
    def make(self):
        # a unit cube centered on 0,0,0
        return cq.Workplane('XY').box(1, 1, 1)

class Thing(Assembly):
    def make(self):
        box1 = Box()
        box2 = Box()

        self.add_constraint(
            # box1 10mm up, no change to rotation
            LockConstraint(box1, Mate(0, 0, 10, (1, 0, 0), (0, 0, 1)))
        )
        self.add_constraint(
            # box2 at origin, rotate around z 45deg ccw
            LockConstraint(box2, Mate(0, 0, 0, (1, 1, 0), (0, 0, 1)))
        )

        return {
            'box_a': box1,
            'box_b': box2,
        }

# Display all of the items that were returned
thing = Thing().make()
for result in thing:
    show_object(result, options={"rgba": (204, 204, 204, 0.0)})