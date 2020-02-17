from flow.core.state import DotDictState


class TestDotDictState:
    def test_state_dot(self):
        state = DotDictState({'test': {'dict': 'val'}})
        assert state.test.dict == 'val'

    def test_state_to_dict(self):
        state = DotDictState({'test': {'dict': 'val'}})
        d = state.to_dict()
        assert d == {'test': {'dict': 'val'}}

    def test_state_update(self):
        state = DotDictState({'test': 'dumb'})
        state.update({'oops': 'my bad'})

        assert state.to_dict() == {'oops': 'my bad', 'test': 'dumb'}

    def test_state_pop(self):
        state = DotDictState({'test': 'dumb'})
        val = state.pop('test')

        assert val == 'dumb'
        assert state.to_dict() == {}

    def test_state_get(self):
        state = DotDictState({'test': 'dumb'})
        val = state.get('test')

        assert val == 'dumb'
        assert state.to_dict() == {'test': 'dumb'}

    def test_nested_dot_get(self):
        state = DotDictState({'test': {'dict': 'val'}})
        assert state.test.get('dict') == 'val'