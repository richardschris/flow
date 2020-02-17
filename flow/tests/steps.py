from flow.actions.examples import PrintAction, CalculateAction, UserInputtedData
from flow.steps import Step, ChoiceStep


class FirstStep(Step):
    def execute(self, *args, **kwargs):
        self.actions = [PrintAction(string='Hello World!'), PrintAction(string='Another String!')]
        return super().execute()


class SecondStep(Step):
    def execute(self, *args, **kwargs):
        state = kwargs.get('state', {})
        value = state.get('value')
        self.actions = [
            PrintAction(string='Doing a calculation'),
            CalculateAction(value=value)
        ]
        return super().execute(*args, **kwargs)


class ThirdStep(Step):
    def execute(self, *args, **kwargs):
        self.actions = [PrintAction(string='We picked this step!')]
        return super().execute()


class PickMeStep(ChoiceStep):
    def _evaluator_func(self, *args, **kwargs):
        if self.state.get('skip_me') is True:
            return ThirdStep()
        else:
            return SecondStep()