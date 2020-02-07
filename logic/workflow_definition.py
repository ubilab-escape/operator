from workflow import *                                       # noqa ignore=F405
from message import State


class WorkflowDefinition:

    def create(self, settings):
        participants = 4
        if settings:
            participants = settings['participants']

        return [
            # Init
            InitWorkflow([
                SendTriggerWorkflow("Reset safe",
                                    "5/safe/control", State.OFF),
                SendTriggerWorkflow("Reset scale",
                                    "6/puzzle/scale", State.OFF),
                SendTriggerWorkflow("Close lab room door",
                                    "4/door/entrance", State.OFF),
                SendTriggerWorkflow("Close server room door",
                                    "4/door/server", State.OFF),
                SendTriggerWorkflow("Deactivate laser",
                                    "7/laser", State.OFF),
                SendTriggerWorkflow("Deactivate laser",
                                    "7/laser", State.OFF),
                LabRoomLightControlWorkflow(State.OFF),
                ServerRoomLightControlWorkflow(State.OFF)
            ]),
            SequenceWorkflow("Entrance room", [
                # First puzzle
                Workflow("Input keypad code", "4/puzzle"),
                # Open door after successfully solved previous puzzle
                SendTriggerWorkflow("Open lab room door",
                                    "4/door/entrance", State.ON),
                # Second puzzle for closing lab door
                Workflow("Globes riddle", "4/globes", {'data': participants}),
                LabRoomLightControlWorkflow(State.ON)
            ]),
            # Allow multiple riddles in lab room
            ParallelWorkflow("Lab room", [
                SequenceWorkflow("Solve safe", [
                    Workflow("Activate safe", "5/safe/activate"),
                    Workflow("Open safe", "5/safe/control"),
                    ScaleWorkflow("Scale riddle", "6/puzzle/scale")
                ]),
                SequenceWorkflow("Solve door riddle", [
                    SendTriggerWorkflow("Activate laser", "7/laser", State.ON),
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
                    ServerRoomLightControlWorkflow(State.ON, 100),
                    Workflow("Control robot", "7/robot"),
                    SendTriggerWorkflow("Open server room door",
                                        "4/door/server", State.ON),
                    ServerRoomLightControlWorkflow(State.ON)
                ])
            ]),
            SequenceWorkflow("Server room", [
                ParallelWorkflow("Server cabinets", [
                    Workflow("Terminal riddle", "6/puzzle/terminal"),
                    SequenceWorkflow("Left Server cabinet", [
                        Workflow("Maze riddle", "8/puzzle/maze"),
                        Workflow("IP riddle", "8/puzzle/IP")
                    ])
                ]),
                Workflow("Simon riddle", "8/puzzle/simon")
            ]),
            ExitWorkflow([
                SendTriggerWorkflow("Open escape room door",
                                    "4/door/entrance", State.ON),
                ServerRoomLightControlWorkflow(State.ON, 255, (0, 255, 0)),
                LabRoomLightControlWorkflow(State.ON, 255, (0, 255, 0)),
                AudioControlWorkflow(
                    "Play success",
                    "/opt/ue-operator/sounds/success.mp3",
                    True
                )
            ])
        ]
