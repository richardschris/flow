# FLOW - A WORKFLOW LIBRARY/SERVICE

Commonly, developers need to create workflows in applications. Whether this is a step-by-step process, or a divergent "go to this step, and do these actions, skipping this other step", or even tracking a ticket through a flow, there is no common way to do this. This project aims to solve several issues that I've experienced in working with custom workflow systems and provide a general framework for executing and tracking them.

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
