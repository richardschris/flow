from flow.core import Base
from flow.core.mixins import AddStepMixin, WorkflowSearchMixin
from flow.core.exceptions import TooManyNextStepsError
from flow.steps.utils import NextStepChoice


class Step(Base, AddStepMixin, WorkflowSearchMixin):
    """ Base class for steps

    attributes:
     - actions: a list of actions the step performs
     - next_step: the next step
     - state: the state from the workflow
    """
    actions = []
    next_step = None
    state = None

    def __init__(self, next_step=None, state=None, *args, **kwargs):
        """
        params:
         - next_step: the next step to transition to after completion
         - state: the state object (defaults to a dict)
        """
        self.next_step = next_step
        self.state = state or {}
        super().__init__(*args, **kwargs)

    def execute(self, *args, **kwargs):
        """ execute the actions and call the transition function. Any args/kwargs you
        pass in are by default passed to the actions
        """
        for action in self.actions:
            result = action.execute(*args, **kwargs)
            if result:
                self.state.update(result)

        return self.transition()

    def transition(self, next_step=None, *args, **kwargs):
        """ Finish the step. Either return the next step that is passed in, or use the
        next_step property on the step
        """
        if next_step:
            return self.state, next_step
        elif self.next_step:
            return self.state, self.next_step
        else:
            return self.state, None

    def add_action(self, action=None, *args, **kwargs):
        """ Add an action to the action list. """
        if action:
            self.actions.append(action())


class ChoiceStep(Step):
    """ Base class for steps that can have multiple transitions """

    def __init__(self, next_step_selector=None, *args, **kwargs):
        self.next_step_selector = next_step_selector or self._next_step_selector
        super().__init__(*args, **kwargs)

    def transition(self, *args, **kwargs):
        next_step = self.next_step_selector(*args, **kwargs)

        return self.state, next_step

    def _next_step_selector(self, *args, **kwargs):
        raise NotImplementedError


class FixedChoiceStep(ChoiceStep):
    """ Step for selectively transitioning between steps based on an evaluator. Takes
    an array of NextStepChoices and executes the evaluators on them; if one succeeds,
    it transitions to the next step, otherwise, it raises an exception.
    """

    def __init__(self, choices=None, *args, **kwargs):
        """ choices must be a NextStepChoice or an array of NextStepChoices """
        self._choices = []
        choices = choices or []
        if isinstance(choices, NextStepChoice):
            choices = [choices]

        for choice in choices:
            self.add_choice(choice)

        super().__init__(*args, **kwargs)

    def add_choice(self, choice):
        if not isinstance(choice, NextStepChoice):
            raise TypeError
        self._choices.append(choice)

    def _next_step_selector(self, *args, **kwargs):
        """ Internal method for evaluating steps. If multiple evaluators return true, raises
        an exception.
        """
        successful_choices = []
        for choice in self._choices:
            if choice.evaluator(state=self.state, *args, **kwargs):
                successful_choices.append(choice.step)

        if len(successful_choices) != 1:
            raise TooManyNextStepsError

        return successful_choices.pop()
