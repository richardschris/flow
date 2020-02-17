from flow.core.mixins import AddStepMixin


class Workflow(AddStepMixin):
    current_step = None
    state = None

    def __init__(self, first_step=None, state=None, *args, **kwargs):
        self.current_step = first_step
        self.state = state or {}

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
