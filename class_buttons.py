import discord
from discord.ui import Button, View

class InfoButton(Button):
    def __init__(self, emoji, url, row, label='Info', disabled=False):
        super().__init__(label=label, url=url, emoji=emoji, row=row, disabled=disabled)

class ServiceButton(Button):
    def __init__(self, label, emoji, row, disabled=False):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.secondary, row=row, disabled=disabled)
    # function to do:
    # may be "if label == ..."

class ActionButton(Button):
    def __init__(self, label, emoji, row, disabled=False):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.primary, row=row, disabled=disabled)

class GreenButton(Button):
    def __init__(self, label, emoji, row, disabled=False):
        super().__init__(label=label, emoji=emoji, style=discord.ButtonStyle.green, row=row, disabled=disabled)
