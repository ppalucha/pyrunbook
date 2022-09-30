import readline
import sys
from datetime import datetime

from termcolor import colored

from .display import error, progress, list_steps
from .runbook import RunBook
from .step import StepState


class Command(object):
    def __init__(self, description: str, parameters: bool = False, hidden: bool = False):
        self._description: str = description
        self.display: str = self.format()
        self._key: str = self.detect_key()
        self._allow_parameters: bool = parameters
        self.hidden = hidden

    def format(self) -> str:
        return "".join(map(
            lambda char: colored(char.lower(), "yellow", attrs=["reverse"]) if char.isupper() else char,
            self._description
        ))

    def detect_key(self) -> str:
        upper = "".join(filter(lambda char: char.isupper(), self._description))
        assert len(upper) == 1
        return upper.lower()

    def match(self, command: str) -> bool:
        if not self._allow_parameters:
            return command == self._key
        return command.startswith(self._key)

    def run(self, runbook: RunBook, command: str) -> None:
        pass

    @staticmethod
    def update_current(runbook: RunBook) -> None:
        runbook.steps[runbook.current].update_timestamp = datetime.utcnow()

    @staticmethod
    def progress(runbook: RunBook) -> None:
        Command.update_current(runbook)
        runbook.current += 1

    @staticmethod
    def set_state(runbook: RunBook, state: StepState) -> None:
        runbook.steps[runbook.current].state = state
        Command.progress(runbook)


class SetStateCommand(Command):
    def __init__(self, description: str, state: StepState):
        super().__init__(description)
        self.desired_state = state

    def run(self, runbook: RunBook, command: str) -> None:
        super().set_state(runbook, self.desired_state)
        progress("Step", runbook.current + 1, "marked as", self.desired_state.value)


class RunCommand(Command):
    def __init__(self):
        super().__init__("Run")

    def run(self, runbook: RunBook, command: str) -> None:
        super().set_state(runbook, StepState.DONE)


class DoneCommand(SetStateCommand):
    def __init__(self):
        super().__init__("Done", StepState.DONE)


class FailCommand(SetStateCommand):
    def __init__(self):
        super().__init__("Fail", StepState.FAIL)


class SkipCommand(SetStateCommand):
    def __init__(self):
        super().__init__("Skip", StepState.SKIP)


class GotoCommand(Command):
    def __init__(self):
        super().__init__("Goto step", parameters=True)

    def run(self, runbook: RunBook, command: str) -> None:
        if command == "g":
            error("Provide step to go to, for example: g 1")
            return
        if command.startswith("g "):
            goto = command[2:]
        else:
            goto = command[1:]
        try:
            goto_index = int(goto)
        except ValueError:
            error("Incorrect step index", goto)
            return
        if goto_index < 1 or goto_index > len(runbook.steps):
            error("Incorrect step index", goto_index)
            return
        runbook.current = goto_index - 1


class CommentCommand(Command):
    def __init__(self):
        super().__init__("coMment", parameters=True)

    def run(self, runbook: RunBook, command: str) -> None:
        if command == "m":
            readline.set_startup_hook(lambda: readline.insert_text(runbook.steps[runbook.current].comment))
            try:
                runbook.steps[runbook.current].comment = input("comment: ")
            finally:
                readline.set_startup_hook()
        elif command.startswith("m "):
            runbook.steps[runbook.current].comment = command[2:]
            progress("Comment on step", runbook.current, "set to", runbook.steps[runbook.current].comment)
        else:
            error("Unexpected command, use 'm' or 'm comment...'")


class ListCommand(Command):
    def __init__(self):
        super().__init__("List steps")

    def run(self, runbook: RunBook, command: str) -> None:
        list_steps(runbook)


class QuiteCommand(Command):
    def __init__(self):
        super().__init__("Quit")

    def run(self, runbook: RunBook, command: str) -> None:
        sys.exit(0)


class IncorrectCommand(Command):
    def __init__(self):
        super().__init__("Incorrect", hidden=True)

    def run(self, runbook: RunBook, command: str) -> None:
        error("Incorrect command:", command)

    def match(self, command: str) -> bool:
        return True


COMMANDS = [
    RunCommand(),
    Command("Continue running"),
    DoneCommand(),
    FailCommand(),
    SkipCommand(),
    GotoCommand(),
    CommentCommand(),
    ListCommand(),
    QuiteCommand(),
    IncorrectCommand()
]


def visible_commands():
    return filter(lambda command: not command.hidden, COMMANDS)


def all_commands():
    return COMMANDS
