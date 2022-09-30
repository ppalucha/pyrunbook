from dataclasses import dataclass

from .step import Step

TEXT_WIDTH = 100


@dataclass
class RunBook(object):
    steps: list[Step]
    name: str = "RunBook"
    description: str = ""
    current: int = 0
    execution_id: str = ""



# class Runner:
#     def __init__(self, runbook: RunBook, state_path: str = "runbook-state.json"):
#         self._runbook = runbook
#         self._state_path = state_path
#         self.read_state()
#
#     def read_state(self) -> None:
#         load_state(self._state_path, self._runbook)
#         # if not Path(self._state_path).is_file():
#         #     return
#         # with open(self._state_path, "r", encoding="UTF-8") as state_file:
#         #     loaded: RunBook = jsonpickle.decode(state_file.read())
#         # if not isinstance(loaded, RunBook):
#         #     raise RuntimeError("Loaded state is not an instance of a Runbook class")
#         # if loaded.name != self._runbook.name:
#         #     raise RuntimeError(f"Loaded state has runbook name '{loaded.name}', should be '{self._runbook.name}'")
#         # if len(loaded.steps) != len(self._runbook.steps):
#         #     raise RuntimeError(f"Loaded state has runbook has {len(loaded.steps)} steps, should be '{len(self._runbook.steps)}'")
#         # for idx, step in enumerate(loaded.steps):
#         #     for attr in ["name", "command", "type", "command", "parameters"]:
#         #         loaded_attr = step.__getattribute__(attr)
#         #         runbook_attr = self._runbook.steps[idx].__getattribute__(attr)
#         #         if loaded_attr != runbook_attr:
#         #             raise RuntimeError(f"Loaded step has {attr} of step {idx+1} = '{loaded_attr}', should be '{runbook_attr}'")
#         # self._runbook.current = min(loaded.current, len(loaded.steps) - 1)
#         # self._runbook.execution_id = loaded.execution_id
#         # for idx, step in enumerate(loaded.steps):
#         #     self._runbook.steps[idx].state = step.state
#         #     self._runbook.steps[idx].comment = step.comment
#         #     self._runbook.steps[idx].update_timestamp = step.update_timestamp
#
#     def save_state(self) -> None:
#         with open(self._state_path, "w", encoding="UTF-8") as state_file:
#             state_file.write(jsonpickle.encode(self._runbook, indent=2))
#
#     def format_step(self, index: int) -> str:
#         step = self._runbook.steps[index]
#         index: str = colored(f"{index+1:>3}", "cyan")
#         name: str = colored(step.name)
#         state: str = colored(step.state.name, step_state_color(step))
#         return f"{index} [{state}] {name}"
#
#     def list_steps(self) -> None:
#         for idx in range(0, len(self._runbook.steps)):
#             marker: str = colored("*", "blue", attrs=["bold"]) if self._runbook.current == idx else " "
#             print(f"{marker}{self.format_step(idx)}")
#
#     def print_current(self) -> None:
#         print("\n" + colored("CURRENT:", "blue"), self.format_step(self._runbook.current))
#         current_step: Step = self._runbook.steps[self._runbook.current]
#         print(f"  TYPE: {current_step.type.name}")
#         if current_step.comment:
#             print(f"  COMMENT: {current_step.comment}")
#         if current_step.update_timestamp:
#             print(f"  UPDATED: {current_step.update_timestamp}")
#         if current_step.description is not None:
#             print(textwrap.fill(current_step.description, initial_indent="  ", subsequent_indent="  ", width=TEXT_WIDTH))
#
#     @staticmethod
#     def format_command(command: str) -> str:
#         return "".join(map(
#             lambda char: colored(char.lower(), "yellow", attrs=["reverse"]) if char.isupper() else char,
#             command
#         ))
#
#     @staticmethod
#     def prompt() -> str:
#         commands = ["Run", "Continue running", "mark as Done", "mark as Failure", "Goto step", "coMment", "List steps", "Quit"]
#         print("| " + " | ".join(map(Runner.format_command, commands)) + " |")
#         return input(colored("> ", attrs=["blink"]))
#
#     @staticmethod
#     def error(*args) -> None:
#         print(colored("Error:", "red"), colored(" ".join(map(str, args)), "white", "on_red"))
#
#     @staticmethod
#     def progress(*args) -> None:
#         print(colored("# ", "cyan"), end="")
#         print(*args)
#
#     def describe(self) -> None:
#         print("Starting runbook", colored(self._runbook.name, "green"))
#         if self._runbook.description:
#             print("\n", textwrap.fill(self._runbook.description, initial_indent="  ", subsequent_indent="  ", width=TEXT_WIDTH), "\n")
#
#     def run(self) -> None:
#         self.describe()
#         self.list_steps()
#         while True:
#             self.print_current()
#             command = Runner.prompt()
#             if command == 'r':
#                 self._runbook.steps[self._runbook.current].state = StepState.DONE
#                 self._runbook.steps[self._runbook.current].update_timestamp = datetime.datetime.utcnow()
#                 self._runbook.current += 1
#             elif command == 'd':
#                 self._runbook.steps[self._runbook.current].state = StepState.DONE
#                 self._runbook.steps[self._runbook.current].update_timestamp = datetime.datetime.utcnow()
#                 Runner.progress("Step", self._runbook.current, "marked as done")
#                 self._runbook.current += 1
#             elif command == "l":
#                 self.list_steps()
#             elif command == "s":
#                 self._runbook.steps[self._runbook.current].state = StepState.SKIP
#                 self._runbook.steps[self._runbook.current].update_timestamp = datetime.datetime.utcnow()
#                 Runner.progress("Step", self._runbook.current, "marked as skipped")
#                 self._runbook.current += 1
#             elif command == "f":
#                 self._runbook.steps[self._runbook.current].state = StepState.FAIL
#                 self._runbook.steps[self._runbook.current].update_timestamp = datetime.datetime.utcnow()
#                 Runner.progress("Step", self._runbook.current, "marked as failed")
#                 self._runbook.current += 1
#             elif command == "m":
#                 readline.set_startup_hook(lambda: readline.insert_text(self._runbook.steps[self._runbook.current].comment))
#                 try:
#                     self._runbook.steps[self._runbook.current].comment = input("comment: ")
#                 finally:
#                     readline.set_startup_hook()
#             elif command.startswith("m "):
#                 self._runbook.steps[self._runbook.current].comment = command[2:]
#                 Runner.progress("Comment on step", self._runbook.current, "set to", self._runbook.steps[self._runbook.current].comment)
#             elif command.startswith("g"):
#                 if command == "g":
#                     Runner.error("Provide step to go to, for example: g 1")
#                     continue
#                 if command.startswith("g "):
#                     goto = command[2:]
#                 else:
#                     goto = command[1:]
#                 try:
#                     goto_index = int(goto)
#                 except ValueError:
#                     Runner.error("Incorrect step index", goto)
#                     continue
#                 if goto_index < 1 or goto_index > len(self._runbook.steps):
#                     Runner.error("Incorrect step index", goto_index)
#                 else:
#                     self._runbook.current = goto_index - 1
#             elif command == 'q':
#                 break
#             else:
#                 Runner.error("Unknown command:", command)
#             self.save_state()
#             if self._runbook.current >= len(self._runbook.steps):
#                 print(colored("All steps done, finishing.", "green"))
#                 self.list_steps()
#                 break
