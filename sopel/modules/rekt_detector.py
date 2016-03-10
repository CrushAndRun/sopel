import sopel.module
import random

@sopel.module.event('KICK')
@sopel.module.rule('.*')

def rekt(bot, trigger):
    rektlist = ['rektangle', 'tyranosaurus rekt', 'the good, the rekt, and the ugly', 'south by southrekt', 'brektfast', 'rektum', 'erektile issues', 'star trekt', 'rektified', 'wrong rektitude', 'bad direktions', 'indirekt parting']
    rektselection = random.choice(rektlist)

    notrektstring = u'\u2610 not rekt'
    rektstring = u'\u2611 ' + rektselection

    bot.say(notrektstring)
    bot.say(rektstring)
