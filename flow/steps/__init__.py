from flow.core import Base
from flow.core.mixins import AddStepMixin
from flow.steps.utils import evaluator_func, NextStepChoice


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
    def __init__(self, next_step_selector=None, *args, **kwargs):
        self.next_step_selector = next_step_selector or self._next_step_selector
        super().__init__(*args, **kwargs)

    def transition(self, *args, **kwargs):
        next_step = self.next_step_selector(*args, **kwargs)

        return self.state, next_step

    def _next_step_selector(self, *args, **kwargs):
        raise NotImplementedError


class FixedChoiceStep(ChoiceStep):
    def __init__(self, choices=None, *args, **kwargs):
        self._choices = []
        choices = choices or []
        if isinstance(choices, NextStepChoice):
            choices = [choices]
        
        self._choices.extend(choices)
        super().__init__(*args, **kwargs)

    def add_choice(self, choice):
        self._choices.append(choice)

    def _next_step_selector(self, *args, **kwargs):
        successful_choices = []
        for choice in self._choices:
            if choice.evaluator(state=self.state, *args, **kwargs):
                successful_choices.append(choice.step)

        if len(successful_choices) != 1:
            raise Exception
            
        return successful_choices.pop()
