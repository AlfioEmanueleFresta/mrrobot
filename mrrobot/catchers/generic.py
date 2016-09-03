class Catcher(object):

    def __init__(self, logger=None):
        self.logger = logger

    def run(self, callback):
        raise NotImplementedError

    def __str__(self):
        return "<Catcher>"

    def attach_logger(self, logger):
        self.logger = logger

    def callback(self, character, *args, **kwargs):

        if self.logger:
            self.logger.callback(character, *args, **kwargs)

        else:
            raise ValueError("No loggers attached.")