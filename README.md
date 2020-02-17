# FLOW - A WORKFLOW LIBRARY/SERVICE

Commonly, developers need to create workflows in applications. Whether this is a step-by-step process, or a divergent "go to this step, and do these actions, skipping this other step", or even tracking a ticket through a flow, there is no common way to do this. This project aims to solve several issues that I've experienced in working with custom workflow systems and provide a general framework for executing and tracking them. Examples include shopping, enrollment, and ticketing systems. This is not meant as a one size fits all framework, but as a framework within which to build your particular applications.

The core principles of Flow are

1. Allow developers to build workflows flexibly.
2. Allow developers to build workflows composably and quickly.
3. Allow developers to insert this functionality into their existing applications simply.

This is extremely early stage software. As such you shouldn't use it for anything. APIs are obviously subject to significant change, as are core concepts.

## WORKFLOW

A workflow is a Python object. You can create a workflow quickly:

``` python
from flow.workflow import Workflow

workflow = Workflow()
```

This workflow doesn't have a state, or any steps. Let's create that now.

``` python
from flow.steps import Step
from flow.actions.examples import PrintAction

step = Step()
step.actions = [PrintAction(string='Hello, world!')]
step.final_step = True

workflow.current_step = step

workflow.execute_step()
```

This is all you need to do to implement a workflow.

Workflow provides two methods: `execute()` and `execute_step()`. `execute()` runs the entire workflow from start to finish, executing every action. `execute_step()` executes the current step only.

Steps are added not to the workflow, but to the next step. The workflow only knows about the current step. Each step knows only its own state, plus the next step. The 'next step' is flexible: you can control this entirely from code. If, for instance, you're implementing a backend for a series of selection screens, and a user does not need to see a step, then you simply don't send them to it.

## DATA MANIPULATION IN WORKFLOWS

A workflow will generally carry with it a state. Through the process of the workflow, we can update that state, with user-inputted data, or perhaps data pulled in from other sources.

This state is always passed into the step on execution and returned; a step can modify it as it sees fit, this can be passed into steps and modified (it is implicitly passed in as a kwarg `state=self.state`, but this is modifiable). An action can return a result and this updates the state on the step, which is ultimately returned to the workflow. An example action, `UserInputtedData`, can illustrate how this works.

``` python
from flow.steps import Step
from flow.workflow import Workflow
from flow.actions.examples import UserInputtedData

workflow = Workflow()
workflow.current_step = Step()
workflow.current_step.actions = [UserInputtedData()]
workflow.current_step.final_step = True
workflow.execute_step(custom_data={'yolo': 'swag'})
print(workflow.state)
```

## MOVING BETWEEN STEPS

Commonly, you need to move between steps and select which step you want to move to. It is easy to override the `transition()` function that gets called at the end of every step, but you can also inherit from the `ChoiceStep`, which defines an `_evaluator_func()` or can be passed a function at initialization to define the evaluator. This evaluator should execute whatever logic it needs to in order to transition to the correct step.

``` python
from flow.steps import ChoiceStep


class PIckMeStep(ChoiceStep):
    def _evaluator_func(self, *args, **kwargs):
        if self.state.get('skip_me') is True:
            return ThirdStep()
        else:
            return SecondStep()


workflow = Workflow()
choice_step = PIckMeStep()
choice_step.actions = [UserInputtedData()]
workflow.current_step = FirstStep(next_step=choice_step)
workflow.state = {'test_data': 3}
workflow.execute_step()
workflow.execute_step(custom_data={'skip_me': True})
workflow.execute_step()
```

This means that you can have a workflow where a user can click a button and return to a previous step, as well: it is agnostic about what steps are next.

## THE FUTURE

Currently my focus is on core functionality and developer ergonomics. But as I settle on an API and an architecture, things are likely to change dramatically. The goals are, in some semblance of order.

1. Store/retrieve current workflow state in a database.
2. Allow resumption of workflows.
3. Create diagrams of workflows from execution flows.
4. Load workflow schemas from yaml files
