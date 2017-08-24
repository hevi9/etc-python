class Log:
    def __init__(self):
        self._processors = []
        self._log_stack = []
        self._level = 0

    def __call__(self, level: int, *args, **kwargs):
        if level < self._level:
            return
        data = {
            "level": level,
            "vars": kwargs,
        }
        if len(args):
            data["msg"] = " ".join(str(arg) for arg in args)
        data["vars"] = kwargs
        self.process(data)
        return self

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    # enter()
    def scope(self, **kwargs):
        pass

    def setup(self, *processors):
        self._processors = processors

    def process(self, data):
        for processor in self._processors:
            data = processor(data)
        return data


# leave

# program/process scoped log
log = Log()
