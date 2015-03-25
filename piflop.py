# -*- coding: utf-8 -*-
__author__ = 'Dmitry Kryukov'
"""
    PiFlop - music player by floppy drives.
"""

import os
import random
import collections
import types
from cprint import cprint

ParsedCommand = collections.namedtuple('ParsedCommand', ('set', 'command', 'args',), verbose=False)


def _parse_command(cmd):
        """ [cyan]Parse command string into named tuple[/] """
        cmd = cmd.strip(' ')
        cls = ''
        if cmd.startswith('$'):
            cls, cmd = cmd.split(' ', 1)
            cls = cls[1:]
            cmd = cmd.strip(' ')
        cmd += ' '
        cmd, attr = cmd.split(' ', 1)
        attr = attr.strip(' ')
        return ParsedCommand(cls, cmd, attr)


class Shell:
    def __init__(self, asciiart=False, colorize=True):
        self.exit = False
        self.asciiart = list()
        self.colorize = colorize
        self.commands_sets = dict()
        if asciiart and os.path.exists('ASCII.art'):
            with open('ASCII.art') as f:
                asciiart = f.read()
                asciiart = asciiart.split('\n\n')
                asciiart = filter(lambda x:  bool(x.replace('\n', '')), asciiart)
                ascii = list()
                for item in asciiart:
                    ascii.append(cprint('[green]'+item+'[/]', colorize=self.colorize, noprint=True))
            self.asciiart = ascii[:]

        if not self.asciiart:
            art = ('''
             ___________________________.
            |;;|                     |;;||
            |[]|---------------------|[]||
            |;;|                     |;;||
            |;;|                     |;;||
            |;;|                     |;;||
            |;;|                     |;;||
            |;;|                     |;;||
            |;;|                     |;;||
            |;;|_____________________|;;||
            |;;;;;;;;;;;;;;;;;;;;;;;;;;;||
            |;;;;;;_______________ ;;;;;||
            |;;;;;|  ___          |;;;;;||
            |;;;;;| |;;;|         |;;;;;||
            |;;;;;| |;;;|         |;;;;;||
            |;;;;;| |;;;|         |;;;;;||
            |;;;;;| |;;;|         |;;;;;||
            |;;;;;| |___|         |;;;;;||
            \_____|_______________|_____||
            ~~~~~^^^^^^^^^^^^^^^^^~~~~~~
            ''')
            self.asciiart.append(cprint('[green]'+art+'[/]', colorize=self.colorize, noprint=True))
        self.line = 'piflop# '
        self.reserved_commands = ['help']

    # EXIT
    def _exit(self, *args):
        self.exit = True

    def _quit(self, *args):
        self._exit()

    def _bye(self, *args):
        self._exit()

    def _help(self, args=None):
        print 'hello'

    def register(self, cls):
        """ [cyan]
            Add set of commands
            Added set is a class, with [blue]`get_command`[/] method
            [/]
        """

        # Use instances, not classes
        if isinstance(cls, (type, types.ClassType)):
            cls = cls()
        # TODO Check `get_command` exists
        # TODO tmp = cls.get_command('command')
        # Name dublicates must be changed
        # as 'name_N' where N is number
        cname = cls.__class__.__name__
        changed_name = cname
        count = -1
        while changed_name:
            count += 1
            changed_name = cname + '_' + str(count) if count else changed_name
            if changed_name not in self.commands_sets:
                self.commands_sets[changed_name] = cls
                changed_name = ''

    def unregister(self, set_name=None):
        if set_name is None:
            self.commands_sets = dict()
        else:
            try:
                del self.commands_sets[set_name]
            except KeyError:
                # TODO: Find same names with added numbers
                cprint('[red]Commands set [yellow]`%s`[/] does not exist.[/]' % set_name, colorize=self.colorize)
                cprint('Use [blue]`reg -l`[/] for list of registered sets', colorize=self.colorize)

    def run(self):
        print random.choice(self.asciiart)
        print '\n\n'
        cprint('\n[cyan][underline]PiPlop - Music player by floppy drives. version 0.1[/][/]\n', colorize=self.colorize)
        if not self.commands_sets:
            cprint('[red]No registered commands[/]', colorize=self.colorize)
            cprint('To register set of commands use [blue]`reg`[/]', colorize=self.colorize)
            cprint('[blue]`help reg`[/] for more information\n', colorize=self.colorize)

        while not self.exit:
            try:
                cmd = raw_input(cprint('[green]'+self.line+'[/]', colorize=self.colorize, noprint=True))
            except KeyboardInterrupt:
                cprint('\nPlease, enter [blue]`exit`[/] or [blue]`quit`[/] or [blue]`bye`[/]', colorize=self.colorize)
                continue
            # Empty
            if not cmd:
                continue

            parsed_command = _parse_command(cmd)
            commands = list()
            if parsed_command.set:
                if parsed_command.set in self.commands_sets:
                    commands.append(self.commands_sets[parsed_command.set].getattr(self, '_'+parsed_command.command, None))
                else:
                    cprint('[red]Cant find [blue]`%s`[/] in set [yellow]"%s"[/][/]' % (parsed_command.command, parsed_command.set), colorize=self.colorize)
            elif parsed_command.command in self.reserved_commands:
                commands.append(getattr(self, '_'+parsed_command.command, None))
            else:
                commands.append(getattr(self, '_'+parsed_command.command, None))
                for set_name, set_self in self.commands_sets.items():
                    commands.append(getattr(set_self, '_'+parsed_command.command, None))
            commands = filter(lambda x: x is not None, commands)

            if commands:
                if len(commands) > 1:
                    cprint('Found [blue]%s[/] commands. Use one from list below:' % len(commands), colorize=self.colorize)
                    for command in commands:
                        cprint('[yellow]$%s[/] [red]->[/] [blue]%s[/]' % (command.im_class.__name__, parsed_command.command), colorize=self.colorize)
                else:
                    commands[0](parsed_command.args) if parsed_command.args else commands[0]()
            else:
                cprint('[red]Command [blue]`%s`[/] does not exists![/]' % parsed_command.command, colorize=self.colorize)


if __name__ == '__main__':
    s = Shell()
    s.run()
