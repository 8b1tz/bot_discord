import os

import discord
from database import Base, engine
from discord import app_commands
from dotenv import load_dotenv
from models import (Badge, Enable, Friendship, Group, Handitem, Room, User,
                    UserBadge, UserGroup, UserRoom)

Base.metadata.create_all(bind=engine, tables=[
    Enable.__table__,
    Handitem.__table__,
    User.__table__,
    UserRoom.__table__,
    UserBadge.__table__,
    UserGroup.__table__,
    Friendship.__table__,
    Room.__table__,
    Badge.__table__,
    Group.__table__])

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_SECRET')
id_server = os.getenv('ID_SERVER')


class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                value="support_ticket",
                label="Peça ajuda",
                emoji="🎫"),
            discord.SelectOption(
                value="team_ticket",
                label="Entre para equipe",
                emoji="👷")
        ]
        super().__init__(
            placeholder="Selecione uma opção",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_view:dropdown_help"
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "support_ticket":
            await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket()
            )
        elif self.values[0] == "team_ticket":
            await interaction.response.send_message(
                "O usuário escolheu team",
                ephemeral=True,
                view=CreateTicket()
            )

            
class CreateTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.value = None
    
    @discord.ui.button(
        label="Abrir Ticket",
        style=discord.ButtonStyle.blurple,
        emoji="💬")
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.value = True
        self.stop()

        ticket = None
        for thread in interaction.channel.threads:
            if f"{interaction.user.id}" in thread.name:
                if thread.archived:
                    ticket = thread
                else:
                    await interaction.response.send_message(
                        ephemeral=True,
                        content="Você já está em atendimento")
                    return
        if ticket is not None:
            await ticket.unarchive()
            await ticket.edit(
                name=f"{self.emoji}" +
                f"{interaction.user.name}" +
                f"({interaction.user.id})",
                auto_archive_duration=10080,
                invitable=False)
        else:
            ticket = await interaction.channel.create_thread(
                name=f"{interaction.user.name} ({interaction.user.id})", 
                auto_archive_duration=10080)
            await ticket.edit(invitable=False)      
        await interaction.response.send_message(ephemeral=True, 
                                                content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"✉️ **|** {interaction.user.mention} \
                        ticket criado! \n\n <@1193661140673245276>")


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Dropdown())


class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def setup_hook(self) -> None:
        self.add_view(DropdownView())

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=id_server))
            self.synced = True
        print(f'{self.user}')


aclient = client()
tree = app_commands.CommandTree(aclient)


@tree.command(guild=discord.Object(id=id_server), name='setup')
async def setup(interaction: discord.Interaction):

    embed = discord.Embed(
        colour=discord.Color.gold(),
        title="Central do servidor Habbear",
        description="Aqui você poderá entrar em contato com a equipe Habbear"
    )
    embed.set_image(url="https://github.com/8b1tz/bot_discord/blob/main/app/imgs/wallpaper.png?raw=true")

    await interaction.channel.send(embed=embed, view=DropdownView())


# @tree.command()
# async def enable():
#     pass


# @tree.command()
# async def handitem():
#     pass

aclient.run(TOKEN)
