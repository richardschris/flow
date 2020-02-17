from flow.steps import Step
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


if __name__ == '__main__':
    workflow = Workflow(state={'value': 3})
    workflow.current_step = FirstStep(next_step=SecondStep())
    workflow.execute()

    print(workflow.state)

    workflow = Workflow()
    workflow.current_step = Step()
    workflow.current_step.actions = [UserInputtedData()]
    workflow.current_step.final_step = True
    workflow.execute_step(custom_data={'yolo': 'swag'})