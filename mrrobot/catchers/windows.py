from .generic import Catcher as GenericCatcher


class Catcher(GenericCatcher):

    def __init__(self, *args, **kwargs):
        super(Catcher, self).__init__(*args, **kwargs)

    def run(self):

        import pyHook
        import pythoncom

        def _callback(x):
            character = chr(x.Ascii)
            if character and x.Ascii != 0:
                self.callback(character=character)
            return True

        manager = pyHook.HookManager()
        manager.KeyUp = _callback
        manager.HookKeyboard()
        pythoncom.PumpMessages()
