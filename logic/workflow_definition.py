from workflow import Workflow
from workflow import ParallelWorkflow
from workflow import DoorWorkflow
from workflow import SequenceWorkflow
from workflow import ActivateLaserWorkflow
from workflow import ScaleWorkflow
from message import State


class WorkflowDefinition:

    def create(self):
        return [
            # First puzzle
            Workflow("Input keypad code", "4/door/entrance/puzzle"),
            # Open door after successfully solved previous puzzle
            DoorWorkflow("Open door", "4/door/entrance", State.ON),
            # Second puzzle for closing lab door
            Workflow("Globes riddle",
                     "4/puzzle", {'data': 4}),
            # Allow multiple riddles in lab room
            ParallelWorkflow("Lab room", [
                SequenceWorkflow("Solve safe", [
                    Workflow("Activate safe", "5/safe/activate"),
                    Workflow("Open safe", "5/safe/control"),
                    ScaleWorkflow("Scale riddle", "6/puzzle/scale")
                ]),
                SequenceWorkflow("Solve door riddle", [
                    ActivateLaserWorkflow("Activate laser", "7/laser"),
                    ParallelWorkflow("Solve fuse box", [
                        Workflow("Redirect laser in fusebox",
                                 "7/fusebox/laserDetection"),
                        Workflow("First rewiring of fusebox",
                                 "7/fusebox/rewiring0"),
                        Workflow("Second rewiring of fusebox",
                                 "7/fusebox/rewiring1"),
                        Workflow("Set potentiometer of fusebox",
                                 "7/fusebox/potentiometer")
                    ]),
                    Workflow("Control robot", "7/robot")
                ])
            ]),
            # Allow multiple riddles in server room
            ParallelWorkflow("Server room", [
                Workflow("Floppy disk riddle", "6/puzzle/floppy"),
                Workflow("Terminal riddle", "6/puzzle/terminal"),
                Workflow("Maze riddle", "8/puzzle/maze"),
                Workflow("Simon riddle", "8/puzzle/simon")
            ])
        ]
