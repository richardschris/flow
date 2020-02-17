class Step:
    actions = []
    next_step = None
    final_step = False
    state = None

    def __init__(self, next_step=None, state=None, *args, **kwargs):
        self.next_step = next_step
        self.state = state or {}

    def execute(self, *args, **kwargs):
        for action in self.actions:
            result = action.execute(*args, **kwargs)
            if result:
                self.state.update(result)

        return self.transition()

    def transition(self, next_step=None, *args, **kwargs):
        if next_step:
            return self.state, next_step
        elif self.next_step:
            return self.state, self.next_step
        elif self.final_step:
            return self.state, None
        else:
            raise NotImplementedError