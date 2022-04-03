import json
import os
import random
from PIL import Image
import discord

from money import get_users_data, open_account

DIR = 'C:/Users/avcolgate/discord bot/img/captcha'


async def start_job(ctx):

    captcha_name = random.choice(os.listdir(DIR))
    correct = captcha_name[-9:-4]

    print(captcha_name)
    print('correct: ' + correct)

    captcha_path = DIR + "/" + captcha_name
    
    await ctx.channel.send('Your CAPTCHA: ',file=discord.File(captcha_path))

    await open_account(ctx.author)
    users = await get_users_data()
    user = ctx.author

    users[str(user.id)]['captcha'] = correct
    with open('base.json', 'w') as f:
        json.dump(users, f)

    print('in base: ' + users[str(user.id)]['captcha'])






async def guess_captcha(ctx, answer):
    print('answered ' + answer)

    await open_account(ctx.author)
    users = await get_users_data()
    user = ctx.author

    if (users[str(user.id)]['captcha'] == answer):
        print('in base: ' + users[str(user.id)]['captcha'])
        await ctx.channel.send('Correct answer! ✅')
        print('correct answer!!!')

        earnings = random.randrange(40,120)
        await ctx.channel.send(f'you got {earnings} crook bucks to your wallet!')
        users[str(user.id)]['wallet'] += earnings
        with open('base.json', 'w') as f:
            json.dump(users, f)

        await start_job(ctx)


    elif (answer == 'stop'):
        await ctx.channel.send('Thanks for your job!')

    elif (answer == 'skip'):
        await ctx.channel.send('Skipped!')
        await start_job(ctx)

    else:
        print('in base: ' + users[str(user.id)]['captcha'])
        await ctx.channel.send('Wrong answer! ❌\nTry again!')
        print('Wrong answer!!!')
