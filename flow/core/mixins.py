class AddStepMixin:
    def add_step(self, step, *args, **kwargs):
        added_step = False
        if not self.next_step:
            self.next_step = step
        else:
            added_step = self.next_step.add_step(step)

        return self.next_step or added_step
