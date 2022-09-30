import datetime
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class StepType(str, Enum):
    MANUAL = "manual"
    FUNCTION = "function"
    SHELL = "shell"


class StepState(str, Enum):
    TODO = "todo"
    DONE = "done"
    FAIL = "failed"
    SKIP = "skipped"


STATE_COLORS = {
    StepState.TODO: "white",
    StepState.DONE: "green",
    StepState.FAIL: "red",
    StepState.SKIP: "yellow",
}


@dataclass
class Step(object):
    name: str
    description: str = ""
    type: StepType = StepType.MANUAL
    command: Optional[str] = None
    parameters: Optional[list[str]] = None
    state: StepState = StepState.TODO
    comment: str = ""
    update_timestamp: Optional[datetime.datetime] = None


def step_state_color(step: Step):
    return STATE_COLORS[step.state]
