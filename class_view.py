from sqlite3 import Row
import discord
from discord.ui import Button, View
from class_buttons import *
from job import start_job
from money import *

#________________________________________________________GAME START VIEW________________________________________________
def start_gameView(ctx):
    view = View(timeout=0)

    button_start = GreenButton(label='START', emoji="🎮", row=0)
    async def button_start_callback(interaction):
        await interaction.response.send_message(content='Sup, ' + ctx.author.name + '!\nWelcome to the Cyber Crook City!',
        view=mainView(ctx),
        ephemeral=True)
    button_start.callback=button_start_callback
    view.add_item(button_start)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=NHj7YqsmBsM", row=0, emoji='ℹ️')
    view.add_item(button_help_main)

    return view

#________________________________________________________MAIN VIEW________________________________________________
def mainView(ctx):
    view = View(timeout=0)

    button_personalities = ActionButton(label='Personalities', emoji="🦸", row=0)
    async def button_personalities_callback(interaction):

        have_bandit    = " (don't have)"
        have_mercenary = " (don't have)"
        have_boss      = " (don't have)"
        have_hacker    = " (don't have)"

        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]

            if type_ == "personality":
                if name_ == "person_bandit":
                    have_bandit = ""
                if name_ == "person_mercenary":
                    have_mercenary = ""
                if name_ == "person_boss":
                    have_boss = ""
                if name_ == "person_hacker":
                    have_hacker = ""

        embed=discord.Embed(title="Showing your characters", url="https://cybercrooks.xyz/",
        color=discord.Color.blue())
        embed.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")

        embed.add_field(name="-bandit" + have_bandit,       value="shows your *bandit*",    inline=False)
        embed.add_field(name="-mercenary" + have_mercenary, value="shows your *mercenary*", inline=False)
        embed.add_field(name="-boss" + have_boss,           value="shows your *boss*",      inline=False)
        embed.add_field(name="-hacker" + have_hacker,       value="shows your *hacker*",    inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)
    button_personalities.callback=button_personalities_callback
    view.add_item(button_personalities)

    button_work = ActionButton(label='Work', emoji="🏭", row=0)
    async def button_work_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CAPTCHA===\n \
    **-guess <answer>** — make a prediction\n \
    example: **-guess 25p2m**\n\
    **-guess skip** — skip current CAPTCHA\n\
    **-guess stop** — finish the job", view=workView(ctx))
    button_work.callback=button_work_callback
    view.add_item(button_work)

    #button_business = ActionButton(label='Business', emoji="💰", row=0)
    #view.add_item(button_business)

    button_store = ActionButton(label='Store', emoji="🏪", row=0)
    async def button_store_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS STORE=== \
        \n**-buy *item_name***\t to buy items\n**-active *item_name***\t to activate", view=storeView(ctx))
    button_store.callback=button_store_callback
    view.add_item(button_store)

    
    button_bag = ActionButton(label='Bag', emoji="🎒", row=1)
    async def button_bag_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS BAG===", view=bagView(ctx))
    button_bag.callback=button_bag_callback
    view.add_item(button_bag)

    #button_rating = ActionButton(label='Rating', emoji="📃", row=1)
    #view.add_item(button_rating)

    button_casino = ActionButton(label='Casino', emoji="🎲", row=1)
    async def button_casino_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CASINO===", view=casinoView(ctx))
    button_casino.callback=button_casino_callback
    view.add_item(button_casino)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=NHj7YqsmBsM", row=1, emoji='ℹ️')
    view.add_item(button_help_main)

    return view

# ________________________________________________________CASINO VIEW_______________________________________________________
def casinoView(ctx):
    view = View(timeout=0)

    button_roulette = ActionButton(label='Roulette', emoji="⏳", row=0)
    view.add_item(button_roulette)

    button_slots = ActionButton("Slots", "🎰", row=0)
    async def button_slots_callback(interaction):
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)
        bal = bal[0]
        users = await get_users_data()
        user = ctx.author
        bet = users[str(user.id)]['bet']
        await interaction.response.edit_message(content=f"===SLOTS===\nYou have {bal} crook bucks.\nYour bet: {bet} crook bucks", view=slotsView(ctx))
    button_slots.callback=button_slots_callback
    view.add_item(button_slots)

    button_dice = ActionButton(label='Dice', emoji="⏳", row=0)
    view.add_item(button_dice)

    button_back = ServiceButton("Go back", "🔙", row=1)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CITY===", view=mainView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=anH4guiwsPU", row=1, emoji='ℹ️')
    view.add_item(button_help_main)

    return view

# ________________________________________________________SLOTS VIEW_______________________________________________________
def slotsView(ctx):
    view = View(timeout=0)

    button_decrease = ActionButton("x0.5", "⬇️", row=0)
    async def button_decrease_callback(interaction):
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)
        bal = bal[0]
        bet = await change_bet(ctx, 'decrease')
        await interaction.response.edit_message(content=f"===SLOTS===\nYou have {bal} crook bucks.\nYour bet: {bet} crook bucks")
    button_decrease.callback=button_decrease_callback
    view.add_item(button_decrease)

    button_start = GreenButton("Start", "🤑", row=0)
    async def button_bet_callback(interaction):
        await open_account(ctx.author)
        users = await get_users_data()
        user = ctx.author
        await command_slots(ctx, users[str(user.id)]['bet'])
        bal = await update_bank(ctx.author)
        bal = bal[0]
        bet = users[str(user.id)]['bet']
        
        # поменяно на send (чтобы не уезжало) и изменяется view
        await interaction.response.send_message(content=f"===SLOTS===\nYou have {bal} crook bucks.\nYour bet: {bet} crook bucks", view = slotsView(ctx))
    button_start.callback=button_bet_callback
    view.add_item(button_start)

    button_increase = ActionButton("x2", "⬆️", row=0)
    async def button_increase_callback(interaction):
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)
        bal = bal[0]
        bet = await change_bet(ctx, 'increase')
        await interaction.response.edit_message(content=f"===SLOTS===\nYou have {bal} crook bucks.\nYour bet: {bet} crook bucks")
    button_increase.callback=button_increase_callback
    view.add_item(button_increase)

    button_back = ServiceButton("Back", "🔙", row=1)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CASINO===", view=casinoView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)


    button_allin = GreenButton("All in", "🤪", row=1)
    async def button_allin_callback(interaction):
        await open_account(ctx.author)
        bal = await update_bank(ctx.author)
        bal = bal[0]
        bet = await change_bet(ctx, 'allin')
        await interaction.response.edit_message(content=f"===SLOTS===\nYou have {bal} crook bucks.\nYour bet: {bet} crook bucks")
    button_allin.callback=button_allin_callback
    view.add_item(button_allin)
    

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=TiE9pWAwYOs", row=1, emoji='ℹ️')
    view.add_item(button_help_main)



    return view

#________________________________________________________STORE VIEW________________________________________________
def storeView(ctx):
    view = View(timeout=0)

    button_catalog = InfoButton(label='Catalog', emoji="👕", url="https://cybercrooks.xyz/wear", row=0)
    view.add_item(button_catalog)

    button_back = ServiceButton("Go back", "🔙", row=1)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CITY===", view=mainView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=_6FPFNxXdEk", row=1, emoji='ℹ️')
    view.add_item(button_help_main)

    return view

#________________________________________________________BAG VIEW________________________________________________
def bagView(ctx):
    view = View(timeout=0)

    button_colorbag = ActionButton(label="Nickname colors", emoji="🎨", row=0)
    async def button_colorbag_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **nickname colors**", url="https://cybercrooks.xyz/",
        color=discord.Color.gold())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: nickname_color_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'

            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"
                
            if type_ == "nickname_color":
                #обрезка имени
                #name_= name_[name_.find("nickname_color_") + 15:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_colorbag.callback=button_colorbag_callback
    view.add_item(button_colorbag)

    button_backgrbag = ActionButton(label="Backgrounds", emoji="🌆", row=0)
    async def button_backgrbag_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **backgrounds**", url="https://cybercrooks.xyz/",
        color=discord.Color.dark_gold())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: background_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'

            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if type_ == "background":
                #обрезка имени
                #name_= name_[name_.find("background_") + 11:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_backgrbag.callback=button_backgrbag_callback
    view.add_item(button_backgrbag)

    button_banditbag = ActionButton(label="Bandit", emoji="🥷", row=1)
    async def button_banditbag_callback(interaction):
        await interaction.response.edit_message(content="\
    Choose type of your **bandit's** items:",
    view=banditAllView(ctx))
    button_banditbag.callback=button_banditbag_callback
    view.add_item(button_banditbag)

    button_mercenarybag = ActionButton(label="Mercenary", emoji="💥", row=1)
    async def button_mercenarybag_callback(interaction):
        await interaction.response.edit_message(content="\
    Choose type of your **mercenary's** items:",
    view=mercenaryAllView(ctx))
    button_mercenarybag.callback=button_mercenarybag_callback
    view.add_item(button_mercenarybag)

    button_bossbag = ActionButton(label="Boss", emoji="💰", row=1, disabled=True)
    view.add_item(button_bossbag)

    button_hackerbag = ActionButton(label="Hacker", emoji="💻", row=1, disabled=True)
    view.add_item(button_hackerbag)

    button_back = ServiceButton("Go back", "🔙", row=2)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CITY===", view=mainView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=_6FPFNxXdEk", row=2, emoji='ℹ️')
    view.add_item(button_help_main)

    return view

# ________________________________________________________WORK VIEW_______________________________________________________
def workView(ctx):
    view = View(timeout=0)

    button_back = ServiceButton("Go back", "🔙", row=0)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS CITY===", view=mainView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)

    button_start_job = GreenButton("Start", "⚒️", row=0)
    async def button_start_job_callback(interaction):
        await start_job(ctx)
    button_start_job.callback=button_start_job_callback
    view.add_item(button_start_job)


    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=TiE9pWAwYOs", row=0, emoji='ℹ️')
    view.add_item(button_help_main)

    return view


# ________________________________________________________BANDIT ALL VIEW_______________________________________________________
def banditAllView(ctx):
    view = View(timeout=0)

    button_bandit_all_head = ActionButton("Head", "😎", row=0)
    async def button_bandit_all_head_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **bandit** heads", url="https://cybercrooks.xyz/",
        color=discord.Color.red())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: bandit_head_")
        
        
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "bandit" and type_ == "head":
                #обрезка имени
                #name_= name_[name_.find("_head") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_bandit_all_head.callback=button_bandit_all_head_callback
    view.add_item(button_bandit_all_head)

    button_bandit_all_body = ActionButton("Body", "🧥", row=0)
    async def button_bandit_all_body_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **bandit** bodies", url="https://cybercrooks.xyz/",
        color=discord.Color.orange())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: bandit_body_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "bandit" and type_ == "body":
                #обрезка имени
                #name_= name_[name_.find("_body") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_bandit_all_body.callback=button_bandit_all_body_callback
    view.add_item(button_bandit_all_body)

    button_bandit_all_hat = ActionButton("Hat", "🎩", row=0)
    async def button_bandit_all_hat_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []


        em=discord.Embed(title=ctx.author.name + "'s **bandit** hats", url="https://cybercrooks.xyz/",
        color=discord.Color.yellow())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: bandit_hat_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "bandit" and type_ == "hat":
                #обрезка имени
                #name_= name_[name_.find("_hat") + 5:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_bandit_all_hat.callback=button_bandit_all_hat_callback
    view.add_item(button_bandit_all_hat)

    button_bandit_all_hand = ActionButton("Hand", "🔫", row=0)
    async def button_bandit_all_hand_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **bandit** hands", url="https://cybercrooks.xyz/",
        color=discord.Color.green())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: bandit_hand_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "bandit" and type_ == "hand":
                #обрезка имени
                #name_= name_[name_.find("_hand") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_bandit_all_hand.callback=button_bandit_all_hand_callback
    view.add_item(button_bandit_all_hand)

    button_bandit_all_item = ActionButton("Item", "🎈", row=0)
    async def button_bandit_all_item_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **bandit** items", url="https://cybercrooks.xyz/",
        color=discord.Color.blue())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: bandit_item_")

        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "bandit" and type_ == "item":
                #обрезка имени
                #name_= name_[name_.find("_item") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_bandit_all_item.callback=button_bandit_all_item_callback
    view.add_item(button_bandit_all_item)

    button_back = ServiceButton("Go back", "🔙", row=1)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS BAG===", view=bagView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=TiE9pWAwYOs", row=1, emoji='ℹ️')
    view.add_item(button_help_main)

    return view

# ________________________________________________________MERCENARY ALL VIEW_______________________________________________________
def mercenaryAllView(ctx):
    view = View(timeout=0)

    button_mercenary_all_head = ActionButton("Head", "😎", row=0)
    async def button_mercenary_all_head_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **mercanary** heads", url="https://cybercrooks.xyz/",
        color=discord.Color.red())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: mercanary_head_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "mercenary" and type_ == "head":
                #обрез имени
                #name_= name_[name_.find("_head") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_mercenary_all_head.callback=button_mercenary_all_head_callback
    view.add_item(button_mercenary_all_head)

    button_mercenary_all_body = ActionButton("Body", "🧥", row=0)
    async def button_mercenary_all_body_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **mercanary** bodies", url="https://cybercrooks.xyz/",
        color=discord.Color.orange())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: mercanary_body_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "mercenary" and type_ == "body":
                #обрезка имени
                #name_= name_[name_.find("_body") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_mercenary_all_body.callback=button_mercenary_all_body_callback
    view.add_item(button_mercenary_all_body)

    button_mercenary_all_hat = ActionButton("Mask", "🎭", row=0)
    async def button_mercenary_all_hat_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **mercanary** masks", url="https://cybercrooks.xyz/",
        color=discord.Color.yellow())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: mercanary_mask_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "mercenary" and type_ == "mask":
                #обрезка имени
                #name_= name_[name_.find("_mask") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_mercenary_all_hat.callback=button_mercenary_all_hat_callback
    view.add_item(button_mercenary_all_hat)

    button_mercenary_all_hand = ActionButton("Hand", "🔫", row=0)
    async def button_mercenary_all_hand_callback(interaction):
        await open_account(ctx.author)
        user = ctx.author
        users = await get_users_data()

        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []

        em=discord.Embed(title=ctx.author.name + "'s **mercanary** hands", url="https://cybercrooks.xyz/",
        color=discord.Color.green())
        em.set_author(name="Cyber Crooks",
        url="https://twitter.com/CyberCrooksNFT",
        icon_url="http://www.fotolink.su/pic_s/06736607a7c583bb3496f2d844aac222.jpg")
        em.set_footer(text="prefix: mercanary_hand_")
        for thing in bag:
            name_ = thing["name"]
            type_ = thing["type"]
            if type_ != "personality":
                is_active = thing["is_active"]
            else:
                is_active = '\0'
            if type_ != "background" and type_ != "nickname_color":
                person_ = thing["person"]
            else:
                person_ = '\0'
            if is_active == 1:
                is_active = "yes"
            else:
                is_active = "no"

            if person_ == "mercenary" and type_ == "hand":
                #обрезка имени
                #name_= name_[name_.find("_hand") + 6:]
                em.add_field(name=name_, value=f"active: {is_active}")

        await interaction.response.send_message(embed = em, ephemeral=True)
    button_mercenary_all_hand.callback=button_mercenary_all_hand_callback
    view.add_item(button_mercenary_all_hand)

    button_back = ServiceButton("Go back", "🔙", row=1)
    async def button_back_callback(interaction):
        await interaction.response.edit_message(content="===CYBER CROOKS BAG===", view=bagView(ctx))
    button_back.callback=button_back_callback
    view.add_item(button_back)

    button_help_main = InfoButton(url="https://www.youtube.com/watch?v=TiE9pWAwYOs", row=1, emoji='ℹ️')
    view.add_item(button_help_main)

    return view
