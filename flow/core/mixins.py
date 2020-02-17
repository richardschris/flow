class AddStepMixin:
    @property
    def step(self):
        step, _ = self._current_or_next_step
        return step
    
    @step.setter
    def step(self, step_val):
        _, step_attr = self._current_or_next_step
        setattr(self, step_attr, step_val)

    def add_step(self, step, *args, **kwargs):
        added_step = False
        if self.step:
            added_step = self.step.add_step(step)
        else:
            self.step = step

        return added_step or bool(self.step)

    @property
    def _current_or_next_step(self):
        if hasattr(self, 'current_step'):
            return self.current_step, 'current_step'
        elif hasattr(self, 'next_step'):
            return self.next_step, 'next_step'
        else:
            raise NotImplementedError
