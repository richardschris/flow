from flow.core import Base
from flow.workflow import Workflow
from flow.tests.test_workflow import FirstStep


class TestBase:
    def test_base_name(self):
        base = Base(name='foo')
        assert base.name == 'foo'
    
    def test_base_repr(self):
        base = Base(name='foo')
        assert repr(base) == '<Base: foo>'

        workflow = Workflow(name='bar')
        assert repr(workflow) == '<Workflow: bar>'


class TestAddStepMixin:
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