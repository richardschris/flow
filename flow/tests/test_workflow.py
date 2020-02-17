import pytest
from flow.steps import Step, ChoiceStep
from flow.workflow import Workflow
from flow.actions.examples import PrintAction, CalculateAction, UserInputtedData


class FirstStep(Step):
    def execute(self, *args, **kwargs):
        self.actions = [PrintAction(string='Hello World!'), PrintAction(string='Another String!')]
        return super().execute()


class SecondStep(Step):
    final_step = True

    def execute(self, *args, **kwargs):
        state = kwargs.get('state', {})
        value = state.get('value')
        self.actions = [
            PrintAction(string='Doing a calculation'),
            CalculateAction(value=value)
        ]
        return super().execute(*args, **kwargs)


def test_workflow_create():
    workflow = Workflow(state={'value': 3})
    workflow.current_step = FirstStep(next_step=SecondStep())
    workflow.execute()

    assert workflow.state == {'value': 6}


def test_workflow_state_update():
    workflow = Workflow()
    workflow.current_step = Step()
    workflow.current_step.actions = [UserInputtedData()]
    workflow.execute_step(custom_data={'yolo': 'swag'})

    assert workflow.state == {'yolo': 'swag'}


class ThirdStep(Step):
    final_step = True

    def execute(self, *args, **kwargs):
        self.actions = [PrintAction(string='We picked this step!')]
        return super().execute()


class PickMeStep(ChoiceStep):
    def _evaluator_func(self, *args, **kwargs):
        if self.state.get('skip_me') is True:
            return ThirdStep()
        else:
            return SecondStep()


def test_choice_step():
    workflow = Workflow()
    choice_step = PickMeStep()
    choice_step.actions = [UserInputtedData()]
    workflow.current_step = FirstStep(next_step=choice_step)
    workflow.execute_step()
    workflow.execute_step(custom_data={'skip_me': True})
    workflow.execute_step()

    assert isinstance(workflow.current_step, ThirdStep)