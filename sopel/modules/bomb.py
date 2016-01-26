"""
bomb.py - Simple Sopel bomb prank game
Copyright 2012, Edward Powell http://embolalia.net
Licensed under the Eiffel Forum License 2.

http://sopel.dfbta.net
"""
from sopel.module import commands
from random import choice, randint
from re import search
import sched
import time

colors = ['Red', 'Yellow', 'Blue', 'White', 'Black', 'Purple', 'Orange', 'Green']
sch = sched.scheduler(time.time, time.sleep)
fuse = 60  # seconds
bombs = dict()


@commands('bomb')
def start(bot, trigger):
    """
    Put a bomb in the specified user's pants. They will be kicked if they
    don't guess the right wire fast enough.
    """
    if not trigger.group(2):
        return

    if not trigger.sender.startswith('#') or \
       (trigger.nick not in bot.ops and
       trigger.nick not in bot.halfplus):
        return
    global bombs
    global sch
    target = trigger.group(2).split(' ')[0]
    if target in bot.config.other_bots or target == bot.nick:
        return
    if target in bombs:
        bot.say('Must be a banana in ' + target + '\'s pants, I can\'t fit another bomb in there!')
        return
    message = 'Hey, ' + target + '! Don\'t look but, someone put a bomb in your pants...Good luck! 1 minute timer, 8 wires: Red, Yellow, Blue, White, Black, Purple, Orange and Green. Which wire should I cut? Don\'t worry, I know what I\'m doing! (respond with .cutwire color)'
    bot.say(message)
    color = choice(colors)
    bot.msg(trigger.nick,
               "Hey, don\'t tell %s, but the %s wire? Yeah, that\'s the one."
               "But shh! Don\'t say anything!" % (target, color))
    code = sch.enter(fuse, 1, explode, (bot, trigger))
    bombs[target.lower()] = (color, code)
    sch.run()


@commands('cutwire')
def cutwire(bot, trigger):
    """
    Tells sopel to cut a wire when you've been bombed.
    """
    global bombs, colors
    target = trigger.nick
    if target.lower() != bot.nick.lower() and target.lower() not in bombs:
        return
    color, code = bombs.pop(target.lower())  # remove target from bomb list
    wirecut = trigger.group(2).rstrip(' ')
    if wirecut.lower() in ('all', 'all!'):
        sch.cancel(code)  # defuse timer, execute premature detonation
        kmsg = ('KICK %s %s : Cutting ALL the wires! *boom* (You should\'ve picked the %s wire.)'
                % (trigger.sender, target, color))
        bot.write([kmsg])
    elif wirecut.capitalize() not in colors:
        bot.say('I can\'t seem to find that wire, ' + target + '! You sure you\'re picking the right one? It\'s not here!')
        bombs[target.lower()] = (color, code)  # Add the target back onto the bomb list,
    elif wirecut.capitalize() == color:
        bot.say('You did it, ' + target + '! PHEW! Good job, you cut the right wire!')
        sch.cancel(code)  # defuse bomb
    else:
        sch.cancel(code)  # defuse timer, execute premature detonation
        kmsg = 'KICK ' + trigger.sender + ' ' + target + \
               ' : No No No, that\'s the wrong one!!1 Got yourself blown up proper, lol. (You should\'ve picked the ' + color + ' wire.)'
        bot.write([kmsg])


def explode(bot, trigger):
    target = trigger.group(1)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           ' : Oh, come on, ' + target + '! You could\'ve at least picked one! Now you\'re dead. (You should\'ve picked the ' + bombs[target.lower()][0] + ' wire.)'
    bot.write([kmsg])
    bombs.pop(target.lower())
