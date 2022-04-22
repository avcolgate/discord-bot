from token import TOKEN
from email.mime import image
from pydoc import cli
from time import sleep
from tkinter.messagebox import YES
import discord
from discord.ui import Button, View
from discord.ext import commands
import json
import os

os.chdir('C:/Users/avcolgate/discord bot')

from job import *
from class_view import *
from class_buttons import *
from money import *
from shop import *
from images_maker import *

#client = discord.Client()

client = commands.Bot(command_prefix = "-")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

# Service command

@client.command()
async def play(ctx):
    view = start_gameView(ctx)
    await ctx.channel.send('Welcome to the Cyber Crook City!\nPress START to start the game!',
    view=view,
    file=discord.File("C:/Users/avcolgate/discord bot/img/welcome_page.png"))

@client.command()
async def start(ctx):
    view = mainView(ctx)
    await welcome_text(ctx, view)

@client.command()
async def balance(ctx):
    await command_balance(ctx)

@client.command()
async def withdraw(ctx, amount = None):
    await command_withdraw(ctx, amount)
    await command_balance(ctx)

@client.command()
async def deposit(ctx, amount = None):
    await command_deposit(ctx, amount)
    await command_balance(ctx)

@client.command()
async def send(ctx, member:discord.Member, amount=None):
    await command_send(ctx, member, amount)
    await command_balance(ctx)

@client.command()
async def slots(ctx, amount = None):
    await command_slots(ctx, amount)
    await command_balance(ctx)

@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        type = item["type"]
        em.add_field(name=name, value = f"${price} \n {type}")

    await ctx.send(embed = em)

@client.command()
async def buy(ctx,item):
    await open_account(ctx.author)
    res = await buy_this(ctx.author,item)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy **{item}**")
            return
        if res[1]==3:
            await ctx.send(f"You already have **{item}** in your bag!")
            return

    await ctx.send(f"You just bought **{item}**!")

@client.command()
async def sell(ctx,item):
    await open_account(ctx.author)
    res = await sell_this(ctx.author,item)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have **{item}** in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have **{item}** in your bag.")
            return

    await ctx.send(f"You just sold **{item}**!")

#delete!!!______________________________________________--
@client.command()
async def bag(ctx):   
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    is_active = "\0"

    em = discord.Embed(title="Bag")
    for item in bag:
        name_ = item["name"]
        type_ = item["type"]

        #if not background and not nickname_color
        if type_ != "background" and type_ != "nickname_color":
            person_ = item["person"]

        # if not personality then we can use active
        if type_ != "personality":
            is_active = item["is_active"]
            if is_active == True:
                is_active = "yes"
            else:
                is_active = "no"

        if (type_ == "personality"):
            em.add_field(name=name_, value=f"type: {type_}")
        elif (type_ == "background" or type_ == "nickname_color"):
            em.add_field(name=name_, value=f"type: {type_}\nactive: {is_active}")
        else:
            em.add_field(name=name_, value=f"type: {type_}\nperson: {person_}\nactive: {is_active}")

    await ctx.send(embed = em)

@client.command()
async def active(ctx,item):
    await open_account(ctx.author)
    res = await active_command(ctx.author,item)

    if "person" in item:
        await ctx.send("You can't activate a **personality**!")
        return
        

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have **{item}** in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have **{item}** in your bag.")
            return

    await ctx.send(f"You just activated **{item}**!")

@client.command()
async def deactivate(ctx,item):
    await open_account(ctx.author)
    res = await deactivate_command(ctx.author,item)

    if "person" in item:
        await ctx.send("You can't deactivate a **personality**!")
        return

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have **{item}** in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have **{item}** in your bag.")
            return

    await ctx.send(f"You just deactivated **{item}**!")

#delete!!!!_______________________________________________________
@client.command()
async def equipment(ctx, person=None):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()

    if person == None:
        await ctx.channel.send(f'Enter the name of person!')
        return

    if person != 'bandit' and person != 'mercenary' and person != 'boss' and \
       person != 'hacker' and person != 'additional':
        await ctx.channel.send(f'Wrong person!')
        return

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title=f"{person} equipment")
    for item in bag:
        name_ = item["name"]
        type_ = item["type"]
        if type_ != "background" and type_ != "nickname_color":
            person_ = item["person"]
        else:
            person_ = 'additional'
        is_active = '\0'
        if type_ != "personality":
            is_active = item["is_active"]

        if (is_active == True and person_ == person) or (person_ == 'additional' and is_active == True):
            em.add_field(name=name_, value=f"type: {type_}")

    await ctx.send(embed = em)

#delete!!!________________
@client.command()
async def person(ctx):   
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="Personalities")
    for item in bag:
        name_ = item["name"]
        type_ = item["type"]

        if type_ == 'personality':
            em.add_field(name=name_, value=f"type: {type_}")

    await ctx.send(embed = em)

@client.command()
async def bandit(ctx):   
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()

    personality = None

    bandit_background = None
    bandit_head = None
    bandit_body = None
    bandit_hat = None
    bandit_hand = None
    bandit_item = None

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    is_active = "\0"
    person_ = "\0"

    for item in bag:
        name_ = item["name"]
        #print(name)
        type_ = item["type"]
        #print(type_)

        #person for items
        if type_ != "background" and type_ != "nickname_color":
            person_ = item["person"]

        # can't equip a person_bandit
        if type_ != "personality":
            is_active = item["is_active"]

        #background
        if type_ == "background" and is_active == True:
            bandit_background = name_
            #print('--read background')

        #color
        if type_ == "nickname_color" and is_active == True:
            color = name_
            #print('--read color')

        #personality
        if type_ == "personality" and person_ == "bandit":
            personality = name_
            #print('--read personality')
        
        if person_ == "bandit" and is_active == True:          

            if type_ == "head":
                bandit_head = name_
            if type_ == "body":
                bandit_body = name_
            if type_ == "hat":
                bandit_hat = name_
            if type_ == "hand":
                bandit_hand = name_
            if type_ == "item":
                bandit_item = name_

    if personality == None:
        await ctx.send("You don't have a **bandit** personality!")
        return
    
    if bandit_head == None or bandit_body == None:
        await ctx.send("You must have at least a **head** and a **body** to display your **bandit**!")
        return

    await ctx.send(f"**head:** {bandit_head},\n**body:** {bandit_body},\n**background:** {bandit_background}, \
    \n**nickname color:** {color},\n**hat:** {bandit_hat},\n**item:** {bandit_item},\n**hand:** {bandit_hand}")

    await image_bandit(ctx, bandit_head, bandit_body, bandit_background, bandit_hat, bandit_item, bandit_hand, color)
    await command_balance(ctx)

@client.command()
async def mercenary(ctx):   
    await open_account(ctx.author)
    user = ctx.author
    users = await get_users_data()

    personality = None

    mercenary_background = None
    mercenary_head       = None
    mercenary_body       = None
    mercenary_mask       = None
    mercenary_hand       = None

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    is_active = "\0"
    person_ = "\0"

    for item in bag:
        name_ = item["name"]
        #print(name)
        type_ = item["type"]
        #print(type_)

        #person for items
        if type_ != "background" and type_ != "nickname_color":
            person_ = item["person"]

        # can't equip a person_mercenary
        if type_ != "personality":
            is_active = item["is_active"]

        #background
        if type_ == "background" and is_active == True:
            mercenary_background = name_
            #print('--read background')

        #color
        if type_ == "nickname_color" and is_active == True:
            color = name_
            #print('--read color')

        #personality
        if type_ == "personality" and person_ == "mercenary":
            personality = name_
            #print('--read personality')
        
        if person_ == "mercenary" and is_active == True:          

            if type_ == "head":
                mercenary_head = name_
            if type_ == "body":
                mercenary_body = name_
            if type_ == "mask":
                mercenary_mask = name_  
            if type_ == "hand":
                mercenary_hand = name_

    if personality == None:
        await ctx.send("You don't have a **mercenary** personality!")
        return
    
    if mercenary_head == None or mercenary_body == None:
        await ctx.send("You must have at least a **head** and a **body** to display your **mercenary**!")
        return

    await ctx.send(f"**head:** {mercenary_head},\n**body:** {mercenary_body},\n**background:** {mercenary_background}, \
    \n**nickname color:** {color},\n**hat:** {mercenary_mask},\n**hand:** {mercenary_hand}")

    await image_mercenary(ctx, mercenary_head, mercenary_body, mercenary_background, mercenary_mask, mercenary_hand, color)
    await command_balance(ctx)

@client.command()
async def guess(ctx,item):
    await guess_captcha(ctx, item)


async def welcome_text(ctx, view):
    await ctx.channel.send('Sup, ' + ctx.author.name + '!\nWelcome to the Cyber Crook City!',
    view=view,
    file=discord.File('C:/Users/avcolgate/discord bot/img/default_person.png'))

client.run(TOKEN)