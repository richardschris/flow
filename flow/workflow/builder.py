from enum import Enum, auto

from flow.workflow import Workflow
from flow.steps import Step, ChoiceStep, FixedChoiceStep


class StepTypes(Enum):
    choice = auto()
    fixed_choice = auto()
    default = auto()


STEP_TYPES = {
    StepTypes.choice: ChoiceStep,
    StepTypes.fixed_choice: FixedChoiceStep,
    StepTypes.default: Step
}


class WorkflowBuilder:
    def __init__(self, workflow=None, *args, **kwargs):
        self.workflow = workflow or WorkflowBuilder.new_workflow(*args, **kwargs)

    @classmethod
    def new_workflow(self, state=None, *args, **kwargs):
        state = state or {}
        workflow = Workflow(state=state, *args, **kwargs)
        return WorkflowBuilder(workflow=workflow)

    def make_step(self, step_type=StepTypes.default, *args, **kwargs):
        step_type_class = STEP_TYPES[step_type]
        self.workflow.add_step(step_type_class(*args, **kwargs))

    def make_action(self, action, *args, **kwargs):
        step = self.workflow.find_last_step()
        if step:
            step.add_action(action, *args, **kwargs)

    def finalize_workflow(self):
        return self.workflow
