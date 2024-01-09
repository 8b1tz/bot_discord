import os

import discord
from database import Base, engine
from discord import app_commands
from dotenv import load_dotenv
from models import (Badge, Enable, Friendship, Group, Handitem, Room, User,
                    UserBadge, UserGroup, UserRoom)

Base.metadata.create_all(bind=engine, tables=[Enable.__table__, Handitem.__table__, User.__table__, UserRoom.__table__, UserBadge.__table__, UserGroup.__table__, Friendship.__table__,
                                              Room.__table__, Badge.__table__, Group.__table__])


id_server = '1187985085249630208'


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=id_server))
            self.synced = True
        print(f'{self.user}')


aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(guild=discord.Object(id=id_server), name='test')
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"Estou funcionando")

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_SECRET')
aclient.run(TOKEN)