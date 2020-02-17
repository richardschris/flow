from flow.actions import Action

class PrintAction(Action):
    def __init__(self, string=None, *args, **kwargs):
        self.string = string

    def execute(self, *args, **kwargs):
        if self.string:
            print(self.string)
        else:
            raise NotImplementedError


class CalculateAction(Action):
    def __init__(self, value=None, *args, **kwargs):
        self.value = value
    
    def execute(self, *args, **kwargs):
        if self.value:
            return {'value': 2 * self.value}
        return None


class UserInputtedData(Action):
    def execute(self, custom_data=None, *args, **kwargs):
        return {'this is custom data': custom_data}
