import textwrap

from termcolor import colored

from .display import list_steps, format_step
from .command import all_commands, visible_commands
from .runbook import RunBook
from .state import State
from .step import Step, step_state_color

TEXT_WIDTH = 100


class Runner:
    def __init__(self, runbook: RunBook, state_path: str = "runbook-state.json"):
        self._runbook = runbook
        self._state = State(state_path)
        self.load_state()

    def load_state(self) -> None:
        self._state.read(self._runbook)

    def save_state(self) -> None:
        self._state.save(self._runbook)

    @staticmethod
    def prompt() -> str:
        print("| " + " | ".join(map(lambda command: command.format(), visible_commands())) + " |")
        return input(colored("> ", attrs=["blink"]))

    def print_current(self) -> None:
        print("\n" + colored("CURRENT:", "blue"), format_step(self._runbook, self._runbook.current))
        current_step: Step = self._runbook.steps[self._runbook.current]
        print(f"  TYPE: {current_step.type.name}")
        if current_step.comment:
            print(f"  COMMENT: {current_step.comment}")
        if current_step.update_timestamp:
            print(f"  UPDATED: {current_step.update_timestamp}")
        if current_step.description is not None:
            print(textwrap.fill(current_step.description, initial_indent="  ", subsequent_indent="  ", width=TEXT_WIDTH))

    def describe(self) -> None:
        print("Starting runbook", colored(self._runbook.name, "green"))
        if self._runbook.description:
            print("\n", textwrap.fill(self._runbook.description, initial_indent="  ", subsequent_indent="  ", width=TEXT_WIDTH), "\n")

    def run(self) -> None:
        self.describe()
        list_steps(self._runbook)
        while True:
            self.print_current()
            command = Runner.prompt()
            for cmd in all_commands():
                if cmd.match(command):
                    cmd.run(self._runbook, command)
                    break
            self.save_state()
            if self._runbook.current >= len(self._runbook.steps):
                print(colored("All steps done, finishing.", "green"))
                list_steps(self._runbook)
                break
