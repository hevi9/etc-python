#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-

# from  https://raw.github.com/gawel/irc3/master/examples/mybot.py

import logging.config
from irc3.plugins.command import command
import irc3


@irc3.plugin
class MyPlugin:
    """A plugin is a class which take the IrcBot as argument
    """

    def __init__(self, bot):
        self.bot = bot
        self.log = self.bot.log

    @irc3.event(irc3.rfc.JOIN)
    def welcome(self, mask, channel):
        """Welcome people who join a channel"""
        bot = self.bot
        if mask.nick != self.bot.nick:
            bot.call_with_human_delay(
                bot.privmsg, channel, 'Welcome %s!' % mask.nick)
        else:
            bot.call_with_human_delay(
                bot.privmsg, channel, "Hi guys!")

    @command
    def echo(self, mask, target, args):
        """Echo command

            %%echo <words>...
        """
        self.bot.privmsg(mask.nick, ' '.join(args['<words>']))

    @irc3.extend
    def my_usefull_command(self):
        """The extend decorator will allow you to call::

            >>> bot.my_usefull_command()

        """


def main():
    # logging configuration
    logging.config.dictConfig(irc3.config.LOGGING)

    # instanciate a bot
    irc3.IrcBot(
        nick='irc3', autojoins=['#test'],
        host='localhost', port=6667, ssl=False,
        includes=[
            'irc3.plugins.core',
            'irc3.plugins.command',
            'irc3.plugins.human',
            __name__,  # this register MyPlugin
        ]).run()

if __name__ == '__main__':
    main()
