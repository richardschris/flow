from flow.steps import Step, ChoiceStep
from flow.workflow import Workflow
from flow.actions.examples import PrintAction, CalculateAction, UserInputtedData


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

        assert workflow.state == {'yolo': 'swag'}


    def test_choice_step(self):
        workflow = Workflow()
        choice_step = PickMeStep()
        choice_step.actions = [UserInputtedData()]
        workflow.current_step = FirstStep(next_step=choice_step)
        workflow.execute_step()
        workflow.execute_step(custom_data={'skip_me': True})
        workflow.execute_step()

        assert isinstance(workflow.current_step, ThirdStep)

    def test_add_step(self, capsys):
        workflow = Workflow()
        workflow.add_step(FirstStep())
        workflow.add_step(FirstStep())
        workflow.execute_step()
        workflow.execute_step()
        captured = capsys.readouterr()
        test_string = '''Hello World!
Another String!
Hello World!
Another String!
'''
        assert captured.out == test_string

    def test_add_step_ret_vals(self):
        workflow = Workflow()
        val1 = workflow.add_step(FirstStep())
        val2 = workflow.add_step(FirstStep())

        assert val1 == True
        assert val2 == True