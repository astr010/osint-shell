import cmd

from module import Module
from google_module import GoogleModule
from http_module import HTTPModule

class OSINTShell(cmd.Cmd):
    # prompt = 'osint-shell (<no data>)$ '
    ruler = '-'
    # modules = [
    #         {'cmd': 'http', 'cls': 'HTTPModule', 'instance': None}
    # ]

    # modules must be implement methods:
    #       - do_<module name> and complete_<module name>
    AVAILABLE_MODULES = {
            'http': 'HTTPModule'
    }

    def do_modules(self, line):
        'list available modules'
        for cmd, cls in self.AVAILABLE_MODULES.iteritems():
            self.print_line('{}: {}'.format(cmd, cls))
        # for mod_data in self.modules:
        #     status = 'not loaded' if mod_data['instance'] == None else 'loaded'
        #     self.print_line('{cmd} ({cls}): {status}'.format(
        #                 cmd=mod_data['cmd'],
        #                 cls=mod_data['cls'],
        #                 status=status))

    # def default(self, line):
        # print 'default: %s' % line
        # args = Module.parse_cmd(line)
        # for mod_data in self.modules:
        #     if args[0] == mod_data['cmd']:
        #         mod_data['instance'] = globals()[mod_data['cls']](self)

    def do_google(self, line):
        'Google manipulation. Use search and suggest services'
        try:
            args = GoogleModule.parse_cmd(line)
            self.current_module = GoogleModule(self)
            self.current_module.execute_method(args[0], args[1:])
        except Exception as e:
            self.print_line(e)

    def complete_google(self, text, line, begidx, endidx):
        return GoogleModule.complete_methods(text)


    def do_http(self, line):
        'HTTP manipulation. Use: http request_get http://www.google.com'
        try:
            args = HTTPModule.parse_cmd(line)
            if self.current_module == None\
                    or not isinstance(self.current_module, HTTPModule):
                self.current_module = HTTPModule(self)

            self.current_module.execute_method(args[0], args[1:])

        except Exception as e:
            print e

    def complete_http(self, text, line, begidx, endidx):
        return HTTPModule.complete_methods(text)

    def normalize_prompt(self):
        str = 'no module loaded' \
                    if self.current_module == None else self.current_module
        self.prompt = 'osint-shell (%s)$ ' % str

    def print_line(self, line):
        print ' [+] %s' % line

    def print_raw(self, raw_text):
        print raw_text

    def postcmd(self, stop, line):
        self.normalize_prompt()
        return cmd.Cmd.postcmd(self, stop, line)

    def preloop(self):
        self.normalize_prompt()

    def do_quit(self, line):
        'Quit OSINT Shell'
        print 'Quitting...'
        return True

    def cmdloop(self, intro=''):
        try:
            self.current_module = None
            cmd.Cmd.cmdloop(self, intro=intro)
        except KeyboardInterrupt as e:
            print '^C'
            self.cmdloop()

