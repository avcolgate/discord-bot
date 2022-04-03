from PIL import Image, ImageDraw, ImageFont
import discord

async def image_bandit(ctx, bandit_head = None, bandit_body = None, bandit_background = None, bandit_hat = None,
                        bandit_item = None, bandit_hand = None, color=None):

    save_path = "./users/" + str(ctx.author.id) + ".png"

    name = ctx.author.name
    font    = ImageFont.truetype('./fonts/Sen-Regular.ttf', size=32)
    water   = Image.open("./img/water.png").convert('RGBA')
    default = Image.open("./img/mainshop/_default.png").convert('RGBA')

    fill = '#ffff'

    if color == "nickname_color_red":
        fill = 	'#D2042D'
    if color == "nickname_color_orange":
        fill = 	'#FF5733'
    if color == "nickname_color_yellow":
        fill = 	'#FFC300'
    if color == "nickname_color_green":
        fill = 	'#14E863'
    if color == "nickname_color_blue":
        fill = 	'#87CEEB'
    if color == "nickname_color_purple":
        fill = 	'#9F2B68'
    if color == "nickname_color_black":
        fill = 	'#28282B'
    if color == "nickname_color_pink":
        fill = 	'#FF69B4'

    if bandit_background != None:
        path = "./img/mainshop/background/" + str(bandit_background) + ".png"
        img_back = Image.open(path).convert('RGBA')
    else:
        img_back = default


    if bandit_head != None:
        path = "./img/mainshop/bandit/head/" + str(bandit_head) + ".png"
        img_head = Image.open(path)
    else:
        img_head = default

    if bandit_body != None:
        path = "./img/mainshop/bandit/body/" + str(bandit_body) + ".png"
        img_body = Image.open(path)
    else:
        img_body = default

    if bandit_hat != None:
        path = "./img/mainshop/bandit/hat/" + str(bandit_hat) + ".png"
        img_hat = Image.open(path)
    else:
        img_hat = default

    if bandit_item != None:
        path = "./img/mainshop/bandit/item/" + str(bandit_item) + ".png"
        img_item = Image.open(path)
    else:
        img_item = default

    if bandit_hand != None:
        path = "./img/mainshop/bandit/hand/" + str(bandit_hand) + ".png"
        img_hand = Image.open(path)
    else:
        img_hand = default

    res1 = Image.alpha_composite(img_back, img_head)
    res2 = Image.alpha_composite(res1, img_body)
    res3 = Image.alpha_composite(res2, img_hat)
    res4 = Image.alpha_composite(res3, img_item)
    res5 = Image.alpha_composite(res4, img_hand)
    output = res5

    output = output.resize((400, 400), Image.ANTIALIAS)
    output = Image.alpha_composite(output, water)
    
    text = ImageDraw.Draw(output)
    text.text(
    (3, -3),
    name,
    font=font,
    fill=fill)

    output.save(save_path)

    await ctx.channel.send('**' + ctx.author.name + "**'s bandit: ", file=discord.File(save_path))


async def image_mercenary(ctx, mercenary_head = None, mercenary_body = None, mercenary_background = None, mercenary_mask = None,
                               mercenary_hand = None, color = None):

    save_path = "./users/" + str(ctx.author.id) + ".png"

    name = ctx.author.name
    font = ImageFont.truetype('./fonts/Sen-Regular.ttf', size=32)
    water = Image.open("./img/water.png").convert('RGBA')
    default = Image.open("./img/mainshop/_default.png").convert('RGBA')

    fill = '#ffff'

    if color == "nickname_color_red":
        fill = 	'#D2042D'
    if color == "nickname_color_orange":
        fill = 	'#FF5733'
    if color == "nickname_color_yellow":
        fill = 	'#FFC300'
    if color == "nickname_color_green":
        fill = 	'#14E863'
    if color == "nickname_color_blue":
        fill = 	'#87CEEB'
    if color == "nickname_color_purple":
        fill = 	'#9F2B68'
    if color == "nickname_color_black":
        fill = 	'#28282B'
    if color == "nickname_color_pink":
        fill = 	'#FF69B4'

    if mercenary_background != None:
        path = "./img/mainshop/background/" + str(mercenary_background) + ".png"
        img_back = Image.open(path).convert('RGBA')
    else:
        img_back = default

    if mercenary_hand != None:
        path = "./img/mainshop/mercenary/hand/" + str(mercenary_hand) + ".png"
        img_hand = Image.open(path).convert('RGBA')
    else:
        img_hand = default

    if mercenary_head != None:
        path = "./img/mainshop/mercenary/head/" + str(mercenary_head) + ".png"
        img_head = Image.open(path).convert('RGBA')
    else:
        img_head = default

    if mercenary_body != None:
        path = "./img/mainshop/mercenary/body/" + str(mercenary_body) + ".png"
        img_body = Image.open(path).convert('RGBA')
    else:
        img_body = default     

    if mercenary_mask != None:
        path = "./img/mainshop/mercenary/mask/" + str(mercenary_mask) + ".png"
        img_mask = Image.open(path).convert('RGBA')
    else:
        img_mask = default

    res1 = Image.alpha_composite(img_back, img_head)
    res2 = Image.alpha_composite(res1, img_body)
    res3 = Image.alpha_composite(res2, img_mask)
    res4 = Image.alpha_composite(res3, img_hand)
    output = res4

    output = output.resize((400, 400), Image.ANTIALIAS)
    output = Image.alpha_composite(output, water)
    
    text = ImageDraw.Draw(output)
    text.text(
    (3, -3),
    name,
    font=font,
    fill=fill)

    output.save(save_path)

    await ctx.channel.send('**' + ctx.author.name + "**'s mercenary: ", file=discord.File(save_path))