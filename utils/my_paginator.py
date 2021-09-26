import discord
from discord import ui


class BasePaginator(ui.View):
	def __init__(self, timeout):
		super().__init__(timeout= timeout)