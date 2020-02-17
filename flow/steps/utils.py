def evaluator_func(*args, **kwargs):
    return False


class NextStepChoice:
    def __init__(self, step=None, evaluator=None, *args, **kwargs):
        self.step = step
        self.evaluator = evaluator or evaluator_func
