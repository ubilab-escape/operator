from workflow import Workflow
from parallel_workflow import ParallelWorkflow


class WorkflowDefinition:

    def get(self):
        return [
            Workflow("Puzzle 1", "QUEUE_Puzzle_1"),
            Workflow("Puzzle 2", "QUEUE_Puzzle_2"),
            Workflow("Puzzle 3", "QUEUE_Puzzle_3"),
            ParallelWorkflow("Parallel puzzle", "QUEUE_Parallel_Puzzle", [
                Workflow("Puzzle 4", "QUEUE_Puzzle_4"),
                Workflow("Puzzle 5", "QUEUE_Puzzle_5")
            ])
        ]
