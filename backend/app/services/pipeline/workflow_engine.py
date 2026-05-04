from typing import List, Dict, Any


class WorkflowEngine:
    def __init__(self):
        self.steps = []
        self.current_step = 0
        self._status = "idle"

    def add_step(self, step):
        self.steps.append(step)

    def execute_step(self, step):
        if isinstance(step, int):
            index = step
            if index >= len(self.steps):
                raise IndexError(f"Step index {index} out of range")
            step_name = self.steps[index]
            self.current_step = index + 1
            if isinstance(step_name, str):
                return f"{step_name} executed"
            return step_name
        if hasattr(step, 'step_name'):
            return {"status": "success", "step": step.step_name}
        if isinstance(step, dict):
            step_type = step.get("type")
            fn = self._get_step_function(step_type)
            if fn:
                return fn(step)
            raise ValueError(f"Unknown step type: {step_type}")
        return {"status": "success"}

    def reset(self):
        self.current_step = 0

    def start(self, steps):
        self.steps = list(steps) if not isinstance(steps, list) else steps
        self.current_step = 0
        self._status = "running"

    def stop(self):
        self._status = "stopped"

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self._status,
            "total_steps": len(self.steps),
            "current_step": self.current_step,
            "steps": self.steps,
        }

    def _get_step_function(self, step_type: str):
        return {
            "data_ingestion": lambda s: {"status": "success", "data": s.get("data")},
            "data_cleaning": lambda s: {"status": "success", "cleaned_data": s.get("data")},
            "modeling": lambda s: {"status": "success", "model": s.get("model")},
            "reporting": lambda s: {"status": "success", "report": s.get("report")},
            "visualization": lambda s: {"status": "success", "visualization": s.get("visualization")},
        }.get(step_type)

    # Backward-compatible aliases
    @property
    def pipeline_steps(self):
        return self.steps

    @property
    def current_step_index(self):
        return self.current_step

    def reset_pipeline(self):
        self.steps = []
        self.current_step = 0
        self._status = "idle"

    def get_pipeline_status(self) -> Dict[str, Any]:
        return self.get_status()

    def execute_pipeline(self) -> List:
        return [self.execute_step(i) for i in range(len(self.steps))]
