from pathlib import Path

import jsonpickle as jsonpickle

from .runbook import RunBook


class State(object):
    def __init__(self, path: str):
        self._path = path

    def read(self, runbook: RunBook) -> None:
        if not Path(self._path).is_file():
            return
        with open(self._path, "r", encoding="UTF-8") as state_file:
            loaded: RunBook = jsonpickle.decode(state_file.read())
        if not isinstance(loaded, RunBook):
            raise RuntimeError("Loaded state is not an instance of a Runbook class")
        if loaded.name != runbook.name:
            raise RuntimeError(f"Loaded state has runbook name '{loaded.name}', should be '{runbook.name}'")
        if len(loaded.steps) != len(runbook.steps):
            raise RuntimeError(f"Loaded state has runbook has {len(loaded.steps)} steps, should be '{len(runbook.steps)}'")
        for idx, step in enumerate(loaded.steps):
            for attr in ["name", "command", "type", "command", "parameters"]:
                loaded_attr = step.__getattribute__(attr)
                runbook_attr = runbook.steps[idx].__getattribute__(attr)
                if loaded_attr != runbook_attr:
                    raise RuntimeError(f"Loaded step has {attr} of step {idx+1} = '{loaded_attr}', should be '{runbook_attr}'")
        runbook.current = min(loaded.current, len(loaded.steps) - 1)
        runbook.execution_id = loaded.execution_id
        for idx, step in enumerate(loaded.steps):
            runbook.steps[idx].state = step.state
            runbook.steps[idx].comment = step.comment
            runbook.steps[idx].update_timestamp = step.update_timestamp

    def save(self, runbook: RunBook) -> None:
        with open(self._path, "w", encoding="UTF-8") as state_file:
            state_file.write(jsonpickle.encode(runbook, indent=2))
