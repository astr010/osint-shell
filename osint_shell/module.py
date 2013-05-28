class Module(object):
    @classmethod
    def complete_methods(cls, text):
        if not text:
            return cls.available_methods()[:]
        else:
            return [n for n in cls.available_methods()
                            if n.upper().startswith(text.upper())]

    @classmethod
    def available_methods(cls):
        return [fn[3:] for fn in dir(cls) if fn.startswith('do_')]

    @classmethod
    def parse_cmd(cls, line):
        return line.split()

    def __init__(self, shell):
        self.shell = shell

    def execute_method(self, method_name, args):
        return getattr(self, 'do_%s' % method_name)(args)
