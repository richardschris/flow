from flow.core import Base
from flow.core.mixins import AddStepMixin, WorkflowSearchMixin


class Workflow(Base, WorkflowSearchMixin, AddStepMixin):
    name = None
    current_step = None
    state = None

    def __init__(self, first_step=None, state=None, *args, **kwargs):
        self.current_step = first_step
        self.set_state(state=state)
        super().__init__(*args, **kwargs)

    def set_state(self, state=None):
        state = state or {}
        self.state = state

    def execute(self, *args, **kwargs):
        state, next_step = self.current_step.execute(state=self.state, *args, **kwargs)
        self.current_step = next_step
        self.state.update(state)

        if self.current_step:
            self.execute(*args, **kwargs)

    def execute_step(self, *args, **kwargs):
        state, next_step = self.current_step.execute(state=self.state, *args, **kwargs)
        if next_step:
            self.current_step = next_step
        self.state.update(state)
