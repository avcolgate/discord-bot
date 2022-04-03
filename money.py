import discord
from discord.ui import Button, View
import json
import os
import random

# showing the balance
async def command_balance(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()

    wallet_amt = users[str(user.id)]['wallet']
    bank_amt = users[str(user.id)]['bank']

    em = discord.Embed(title = f"{ctx.author.name}'s balance", color = discord.Color.red())
    em.add_field(name = 'Wallet balance', value = wallet_amt)
    em.add_field(name = 'Bank balance', value = bank_amt)
    #em.set_image(url="http://www.fotolink.su/v.php?id=206beb733730045535be87a7e422c105")
    await ctx.channel.send(embed = em)

# withdraw BANK -> WALLET
async def command_withdraw(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.channel.send('Enter the amount')
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)

    # [0] is wallet
    # [1] is bank
    if amount>bal[1]:
        await ctx.channel.send('You don\'t have that much money')
        return
    if amount<0:
        await ctx.channel.send('Amount must be positive')
        return

    await update_bank(ctx.author, amount)            # for the wallet
    await update_bank(ctx.author, -1*amount, "bank") # for the bank
    await ctx.channel.send(f'You withdrew {amount} crook bucks!')

# deposit WALLET -> BANK
async def command_deposit(ctx, amount=None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.channel.send('Enter the amount')
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)

    # [0] is wallet
    # [1] is bank
    if amount>bal[0]:
        await ctx.channel.send('You don\'t have that much money')
        return
    if amount<0:
        await ctx.channel.send('Amount must be positive')
        return

    await update_bank(ctx.author, -1*amount)            # for the wallet
    await update_bank(ctx.author, amount, "bank")       # for the bank
    await ctx.channel.send(f'You deposited {amount} crook bucks!')

# sending money through BANK
async def command_send(ctx, member:discord.Member, amount=None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.channel.send('Enter the amount')
        return

    bal = await update_bank(ctx.author)
    amount = int(amount)

    # [0] is wallet
    # [1] is bank
    if amount>bal[1]:
        await ctx.channel.send('You don\'t have that much money')
        return
    if amount<0:
        await ctx.channel.send('Amount must be positive')
        return

    await update_bank(ctx.author, -1*amount, "bank")
    await update_bank(member, amount, "bank")
    await ctx.channel.send(f'You sent {amount} crook bucks!')

# SLOTS
async def command_slots(ctx, amount):
    await open_account(ctx.author)
    if amount == None:
        await ctx.channel.send('Enter the amount')
        return
    
    bal = await update_bank(ctx.author)
    
    if amount == 'all':
        amount = bal[0]
    else:
        amount = int(amount)

    # [0] is wallet
    # [1] is bank
    if amount>bal[0]:
        await ctx.channel.send('You don\'t have that much money')
        return
    if amount<=0:
        await ctx.channel.send('Amount must be positive')
        return

    final = []
    for i in range(3):
        a = random.choice(['🍉', '🍒', '🔫', '🔔'])
        final.append(a)

    await ctx.channel.send(str(final[0])+str(final[1])+str(final[2]))


    if final[0] == final[1] and final[0] == final[2]:
        await update_bank(ctx.author, 4*amount)
        await ctx.channel.send('You won ' + str(4*amount) + ' crook bucks! (x4)')
    elif final[0] == final[1] and final[0] == final[2] and final[0] == '🔫':
        await update_bank(ctx.author, 10*amount)
        await ctx.channel.send('You won ' + str(10*amount) + ' crook bucks! (x10)')
    elif final[0] == final[1] or \
         final[0] == final[2] or \
         final[1] == final[2]:
        await update_bank(ctx.author, 2*amount)
        await ctx.channel.send('You won ' + str(2*amount) + ' crook bucks! (x2)')
    else:
        await update_bank(ctx.author, -1*amount)
        await ctx.channel.send('You lost ' + str(amount) + ' crook bucks!')
       
# opening an account if there is no account
async def open_account(user):
    users = await get_users_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]['wallet'] = 0
        users[str(user.id)]['bank'] = 0
        users[str(user.id)]['bet'] = 50
        users[str(user.id)]['captcha'] = 'Crooks!!'

        users[str(user.id)]['bag']    = []

    # save base
    with open('base.json', 'w') as f:
        json.dump(users, f)
    return True

# getting the users' data
async def get_users_data():
    with open('base.json', 'r') as f:
        users = json.load(f)    
    return users

# adding or substract to the balance
async def update_bank(user, change = 0, mode = 'wallet'):
    users = await get_users_data()

    users[str(user.id)][mode]+=change

    with open('base.json', 'w') as f:
        json.dump(users, f)

    bal = [users[str(user.id)]['wallet'], users[str(user.id)]['bank']]

    return bal

# changing bet
async def change_bet(message, mode):
    await open_account(message.author)
    users = await get_users_data()
    user = message.author

    if mode == 'increase':
        users[str(user.id)]['bet'] = int(users[str(user.id)]['bet']*2)
    elif mode == 'allin':
        users[str(user.id)]['bet'] = int(users[str(user.id)]['wallet'])
    else:
        users[str(user.id)]['bet'] = int(users[str(user.id)]['bet']/2)

    with open('base.json', 'w') as f:
        json.dump(users, f)

    return users[str(user.id)]['bet']
