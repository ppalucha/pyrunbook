from termcolor import colored

from .runbook import RunBook
from .step import step_state_color


def error(*args) -> None:
    print(colored("Error:", "red"), colored(" ".join(map(str, args)), "white", "on_red"))


def progress(*args) -> None:
    print(colored("# ", "cyan"), end="")
    print(*args)


def format_step(runbook: RunBook, index: int) -> str:
    step = runbook.steps[index]
    index: str = colored(f"{index+1:>3}", "cyan")
    name: str = colored(step.name)
    state: str = colored(step.state.name, step_state_color(step))
    return f"{index} [{state}] {name}"


def list_steps(runbook: RunBook) -> None:
    for idx in range(0, len(runbook.steps)):
        marker: str = colored("*", "blue", attrs=["bold"]) if runbook.current == idx else " "
        print(f"{marker}{format_step(runbook, idx)}")
