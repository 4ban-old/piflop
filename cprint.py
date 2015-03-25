# -*- coding: utf-8 -*-
"""
    Color print function.
    Use: cprint('text', colorize=True) or
         cprint('text %s' % var, colorize=True)
    Can't: cprint('text', var, colorize=True)
"""


class Stack:
    def __init__(self):
        self.items = []

    def isempty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else ''

    def peek(self):
        return self.items[len(self.items)-1] if self.items else None

    def size(self):
        return len(self.items)


def cprint(text, colorize=False, noprint=False):
    """
        Function for color print.
        Use: cprint('text', colorize=True) or
             cprint('text %s' % var, colorize=True) or
             cprint('text %s %s %s' % (var1, var2, var3), colorize=True)

        Can't use: cprint('text', var, colorize=True)
    :param text: String like 'hello world'
    :param colorize: Boolean
    """
    import re
    s = Stack()
    colors = {None: '\033[0m',
              '[black]': '\033[30m',
              '[red]': '\033[31m',
              '[green]': '\033[32m',
              '[yellow]': '\033[33m',
              '[blue]': '\033[34m',
              '[purple]': '\033[35m',
              '[cyan]': '\033[36m',
              '[underline]': '\033[4m'}
    if colorize:
        text = text.split('[/]')
        _text = ''
        for block in text:
            tags = re.findall(r'\[[^\]]{,}\]', block)
            for tag in tags:
                if tag in colors:
                    block = block.replace(tag, colors[tag])
                    s.push(tag)
            if s.peek() in ['[underline]']:
                _text += block + colors[s.peek()]+'\033[24m'
                s.pop()
            else:
                s.pop()
                _text += block + colors[s.peek()]
        text = _text
        text = re.sub(r'\s+^\n', ' ', text)
        if noprint:
            return text
        else:
            print text
    else:
        text = re.sub(r'\[.*?\]', '', text)
        text = re.sub(r'\s+^\n', ' ', text)
        if noprint:
            return text
        else:
            print text