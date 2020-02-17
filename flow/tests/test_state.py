from flow.core.state import DotDictState


def test_state():
    state = DotDictState({'test': {'dict': 'val'}})
    assert state.test.dict == 'val'

    d = state.to_dict()
    assert d == {'test': {'dict': 'val'}}
