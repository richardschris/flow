from flow.steps import Step, ChoiceStep
from flow.workflow import Workflow
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

    def test_dict_state_in_workflow(self):
        workflow = Workflow(state=DotDictState({'value': 3}))
        workflow.current_step = SecondStep()
        workflow.execute_step()

        assert workflow.state.state == {'value': 6}