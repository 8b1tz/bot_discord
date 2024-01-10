import os

import discord
from database import Base, engine
from discord import app_commands
from discord.ext import commands
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

            embed = discord.Embed(
            colour=discord.Color.gold(),
            title="Escolha para qual cargo você gostaria de se candidatar",
            description="Escolha uma das opções abaixo para se candidatar ao cargo desejado:"
        )

        embed.add_field(
            name="Promotor",
            value="Este cargo é responsável por divulgar eventos e atividades, promovendo e atraindo participantes para as atividades do servidor."
        )

        embed.add_field(
            name="Programador",
            value="O cargo de Programador envolve ajudar no desenvolvimento de soluções tecnológicas e ferramentas para o servidor, contribuindo com código e ideias inovadoras."
        )

        embed.add_field(
            name="Conteúdo",
            value="A posição de Conteúdo é ideal para aqueles que desejam criar e editar conteúdo, como textos, imagens ou vídeos para os eventos e atividades do servidor."
        )

        embed.add_field(
            name="Marketing",
            value="Os membros do cargo de Marketing são responsáveis por criar estratégias de marketing e promoção para aumentar a visibilidade e participação nas atividades do servidor."
        )

        embed.add_field(
            name="Locutor",
            value="O cargo de Locutor envolve a narração e apresentação de eventos, criando uma atmosfera envolvente para os participantes durante as atividades do servidor."
        )
        embed.set_image(url="https://github.com/8b1tz/bot_discord/blob/main/app/imgs/wallpaper.png?raw=true")
        await interaction.response.send_message(
            "O usuário escolheu team",
            ephemeral=True,
            view=TicketButtons(),
            embed=embed,
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
@commands.has_permissions(manage_guild=True)
async def setup(interaction: discord.Interaction):

    embed = discord.Embed(
        colour=discord.Color.gold(),
        title="Central do servidor Habbear",
        description="Aqui você poderá entrar em contato com a equipe Habbear"
    )
    embed.set_image(url="https://github.com/8b1tz/bot_discord/blob/main/app/imgs/wallpaper.png?raw=true")

    await interaction.channel.send(embed=embed, view=DropdownView())


@tree.command(guild=discord.Object(id=id_server), name="fecharticket", description="Fecha o ticket")
@commands.has_permissions(manage_guild=True)
async def fecharticket(interaction: discord.Interaction):
    mod = interaction.guild.get_role(1193661140673245276)
    try:
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.role:
            await interaction.channel.delete()
        else:
            await interaction.response.send_message("Isso não pode ser feito")
    except Exception as e:
        await interaction.response.send_message(e)


@tree.command(guild=discord.Object(id=id_server), name='enable')
async def enable(interaction: discord.Interaction):
    await interaction.response.send_message('teste enable')


@tree.command(guild=discord.Object(id=id_server), name='handitem')
async def handitem(interaction: discord.Interaction):
    await interaction.response.send_message('teste handitem')


async def create_ticket(interaction, ticket_type):
    ticket = None
    for thread in interaction.channel.threads:
        if f"{interaction.user.id}" in thread.name:
            if thread.archived:
                ticket = thread
            else:
                await interaction.response.send_message(
                    ephemeral=True,
                    content="Você já está em atendimento"
                )
                return
    else:
        ticket = await interaction.channel.create_thread(
            name=f"Equipe {ticket_type} - {interaction.user.name} ({interaction.user.id})"
        )

    await interaction.response.send_message(
        ephemeral=True,
        content=f"Criei um ticket de {ticket_type.lower()} para você! {ticket.mention}"
    )
    await ticket.send(
        f"✉️ **|** {interaction.user.mention} ticket criado! \n\n <@1193661140673245276>"
    )


class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        button_data = [
            {"label": "Promotor", "custom_id": "promotor_ticket"},
            {"label": "Programador", "custom_id": "programador_ticket"},
            {"label": "Conteúdo", "custom_id": "conteudo_ticket"},
            {"label": "Marketing", "custom_id": "marketing_ticket"},
            {"label": "Locutor", "custom_id": "locutor_ticket"}
        ]

        for data in button_data:
            button = discord.ui.Button(
                label=data["label"],
                style=discord.ButtonStyle.blurple,
                custom_id=data["custom_id"]
            )
            self.add_item(button)



aclient.run(TOKEN)
