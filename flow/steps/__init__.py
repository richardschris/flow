from flow.core import Base
from flow.core.mixins import AddStepMixin


class Step(Base, AddStepMixin):
    actions = []
    next_step = None
    final_step = False
    state = None

    def __init__(self, next_step=None, state=None, *args, **kwargs):
        self.next_step = next_step
        self.state = state or {}
        super().__init__(*args, **kwargs)

    def execute(self, *args, **kwargs):
        for action in self.actions:
            result = action.execute(*args, **kwargs)
            if result:
                self.state.update(result)

        return self.transition()

    def transition(self, next_step=None, *args, **kwargs):
        if next_step:
            return self.state, next_step
        elif self.next_step:
            return self.state, self.next_step
        else:
            return self.state, None

    def add_action(self, action=None):
        added_action = False
        if action:
            self.actions.extend(action)
            added_action = True
        
        return added_action


class ChoiceStep(Step):
    def __init__(self, evaluator=None, *args, **kwargs):
        self.evaluator = evaluator or self._evaluator_func
        super().__init__(*args, **kwargs)

    def transition(self, *args, **kwargs):
        next_step = self.evaluator(*args, **kwargs)

        return self.state, next_step

    def _evaluator_func(self, *args, **kwargs):
        raise NotImplementedError
