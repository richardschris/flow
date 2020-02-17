from flow.core import Base


class State(Base):
    def __init__(self, *args, **kwargs):
        self._state = None

    def __getitem__(self, item, *args, **kwargs):
        raise NotImplementedError

    def __getattr__(self, attr, *args, **kwargs):
        raise NotImplementedError

    def __setitem__(self, key, value, *args, **kwargs):
        raise NotImplementedError

    def __setattr__(self, key, value, *args, **kwargs):
        raise NotImplementedError

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state=None):
        self._state = state


class DotDictState(State):
    _state = None

    def __init__(self, state=None, *args, **kwargs):
        self._state = {}
        state = state or {}
        self.state.update(state)
        for k, v in state.items():
            if isinstance(v, (dict)):
                self.state[k] = DotDictState(v)
            else:
                self.state[k] = v

    def __getitem__(self, item):
        return self._state[item]

    def __getattr__(self, attr):
        return self._state[attr]

    def __setattr__(self, attr, value):
        if attr == '_state':
            object.__setattr__(self, '_state', value)
        else:
            self._state[attr] = self._to_dict_state(value)

    def __setitem__(self, key, value):
        self._state[key] = self._to_dict_state(value)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state=None):
        self._state.update(state or {})

    def update(self, items):
        for k, v in items.items():
            if isinstance(v, (dict)):
                self._state[k] = DotDictState(v)
            else:
                self._state[k] = v

    def get(self, item):
        if item in self._state:
            return self._state[item]
        else:
            return None

    def pop(self, item):
        if item in self._state:
            value = self._state[item]
            del self._state[item]
            return value
        else:
            return None

    def items(self):
        data = self._state.to_dict()
        return data.items()

    def to_dict(self):
        data = {}
        for k, v in self._state.items():
            if isinstance(v, DotDictState):
                data[k] = v.to_dict()
            else:
                data[k] = v
        return data

    def _to_dict_state(self, data):
        if not isinstance(data, (dict, DotDictState)):
            return data
        return DotDictState(state=data)
