import pytest

from flow.core.exceptions import TooManyNextStepsError
from flow.steps import Step, ChoiceStep
from flow.workflow import Workflow
from flow.steps import FixedChoiceStep
from flow.steps.utils import NextStepChoice
from flow.tests.steps import FirstStep, SecondStep, ThirdStep, PickMeStep
from flow.actions.examples import UserInputtedData, CalculateAction
from flow.core.state import DotDictState


class TestWorkflow:
    def test_workflow_create(self):
        workflow = Workflow(state={'value': 3})
        workflow.current_step = FirstStep(next_step=SecondStep())
        workflow.execute()

        assert workflow.state == {'value': 6}


    def test_workflow_state_update(self):
        workflow = Workflow()
        workflow.current_step = Step()
        workflow.current_step.actions = [UserInputtedData()]
        workflow.execute_step(custom_data={'yolo': 'swag'})

        assert workflow.state == {'custom_data': {'yolo': 'swag'}}


    def test_choice_step(self):
        workflow = Workflow()
        choice_step = PickMeStep()
        choice_step.actions = [UserInputtedData()]
        workflow.current_step = FirstStep(next_step=choice_step)
        workflow.execute_step()
        workflow.execute_step(custom_data={'skip_me': True}, flat=True)
        workflow.execute_step()

        assert isinstance(workflow.current_step, ThirdStep)

    def test_fixed_choice_step(self, capsys):
        workflow = Workflow()
        choice_step = FixedChoiceStep()
        choice_step.actions = [UserInputtedData()]
        next_step_1 = NextStepChoice(
            step=FirstStep(), evaluator=lambda state, *args, **kwargs: state.get('test')
        )
        next_step_2 = NextStepChoice(
            step=ThirdStep(), evaluator=lambda state, *args, **kwargs: state.get('success')
        )
        choice_step.add_choice(next_step_1)
        choice_step.add_choice(next_step_2)
        workflow.current_step = choice_step
        workflow.execute_step(custom_data={'success': True}, flat=True)
        workflow.execute_step()
        captured = capsys.readouterr()

        assert captured.out == 'We picked this step!\n'

    def test_bad_fixed_choice_step(self):
        choice_step = FixedChoiceStep()
        next_step = FirstStep()
        with pytest.raises(TypeError):
            choice_step.add_choice(next_step)

    def test_too_many_steps_choice_step(self, capsys):
        workflow = Workflow()
        choice_step = FixedChoiceStep()
        choice_step.actions = [UserInputtedData()]

        def evaluator_1(state, *args, **kwargs):
            return True

        next_step_1 = NextStepChoice(step=FirstStep(), evaluator=evaluator_1)

        def evaluator_2(state, *args, **kwargs):
            return True

        next_step_2 = NextStepChoice(step=ThirdStep(), evaluator=evaluator_2)
        choice_step.add_choice(next_step_1)
        choice_step.add_choice(next_step_2)
        workflow.current_step = choice_step

        with pytest.raises(TooManyNextStepsError):
            workflow.execute_step(custom_data={'success': True}, flat=True)

    def test_dict_state_in_workflow(self):
        workflow = Workflow(state=DotDictState({'value': 3}))
        workflow.current_step = SecondStep()
        workflow.execute_step()

        assert workflow.state.state == {'value': 6}