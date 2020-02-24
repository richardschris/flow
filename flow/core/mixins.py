class AddStepMixin:
    """ Generic mixin for supporting the add_step() method for both Workflows and Steps """
    @property
    def step(self):
        step, _ = self._current_or_next_step
        return step

    @step.setter
    def step(self, step_val):
        _, step_attr = self._current_or_next_step
        setattr(self, step_attr, step_val)

    def add_step(self, step, *args, **kwargs):
        """ Add a step to a workflow or a step. It will traverse the graph
        until it finds a step it can add to.

        params:

        - step - the step (inherits from Step) to be added.
        """
        added_step = False
        if self.step:
            added_step = self.step.add_step(step, *args, **kwargs)
        else:
            self.step = step

        return added_step or bool(self.step)

    @property
    def _current_or_next_step(self):
        """ Internal helper method to work with differently named attributes """
        if hasattr(self, 'current_step'):
            return self.current_step, 'current_step'
        elif hasattr(self, 'next_step'):
            return self.next_step, 'next_step'
        else:
            raise NotImplementedError


class WorkflowSearchMixin:
    def find_last_step(self):
        if self.step:
            return self.step.find_last_step()
        else:
            return self
