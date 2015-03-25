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
from converter import convert

ParsedCommand = collections.namedtuple('ParsedCommand', ('cls', 'cmd', 'param',), verbose=False)


def _parse_command(cmd):
        """Parse command string into named tuple """
        cmd = cmd.strip(' ')
        cls = ''
        if cmd.startswith('@'):
            cls, cmd = cmd.split(' ', 1)
            cls = cls[1:]
            cmd = cmd.strip(' ')
        cmd += ' '
        cmd, param = cmd.split(' ', 1)
        param = param.strip(' ')
        return ParsedCommand(cls, cmd, param)


class Shell:
    def __init__(self, asciiart=False, colorize=True):
        self.exit = False
        self.asciiart = list()
        self.colorize = colorize
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
        self.line = '>>> '
        self.reserved_commands = ['help']

    def _exit(self, *args):
        self.exit = True

    def _quit(self, *args):
        self._exit()

    def _bye(self, *args):
        self._exit()

    def _help(self, args=None):
        print 'hello'

    def run(self):
        print random.choice(self.asciiart)
        print '\n\n'
        cprint('\n[cyan][underline]PiPlop - Music player by floppy drives. version 0.1[/][/]\n', colorize=self.colorize)
        while not self.exit:
            try:
                cmd = raw_input(cprint('[green]'+self.line+'[/]', colorize=self.colorize, noprint=True))
            except KeyboardInterrupt:
                cprint('\nPlease, enter [blue]`exit`[/] or [blue]`quit`[/] or [blue]`bye`[/]', colorize=self.colorize)
                continue
            if not cmd:
                continue

            parsedcommand = _parse_command(cmd)
            commands = list()
            if parsedcommand.set:
                commands.append(parsedcommand.command)
                #if parsedcommand.set in self.commands_sets:
                #    commands.append(self.commands_sets[parsedcommand.set].getattr(self, '_'+parsedcommand.command, None))
                #else:
                #    cprint('[red]Cant find [blue]`%s`[/] in set [yellow]"%s"[/][/]' % (parsedcommand.command, parsedcommand.set), colorize=self.colorize)
            elif parsedcommand.command in self.reserved_commands:
                commands.append(getattr(self, '_'+parsedcommand.command, None))
            else:
                commands.append(getattr(self, '_'+parsedcommand.command, None))
                for set_name, set_self in self.commands_sets.items():
                    commands.append(getattr(set_self, '_'+parsedcommand.command, None))
            commands = filter(lambda x: x is not None, commands)

            if commands:
                if len(commands) > 1:
                    cprint('Found [blue]%s[/] commands. Use one from list below:' % len(commands), colorize=self.colorize)
                    for command in commands:
                        cprint('[yellow]$%s[/] [red]->[/] [blue]%s[/]' % (command.im_class.__name__, parsedcommand.command), colorize=self.colorize)
                else:
                    commands[0](parsedcommand.args) if parsedcommand.args else commands[0]()
            else:
                cprint('[red]Command [blue]`%s`[/] does not exists![/]' % parsedcommand.command, colorize=self.colorize)

if __name__ == '__main__':
    s = Shell()
    s.run()
