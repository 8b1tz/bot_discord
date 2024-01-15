import os

import discord
from database import Base, engine
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from models import (Badge, Enable, Friendship, Group, Handitem, Room, User,
                    UserBadge, UserGroup, UserRoom)
from scripts import get_enable_by_id_or_api, get_hand_item_by_id_or_api

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

TOKEN = 'MTE4MzUzMDAyMDI3NTIzNjkyNA.GGf3kN.MtPR6KDHG_T9FiSDH1kwFmdSO3s_9Ko1kEqTxs'
id_server = '1187985085249630208'


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
                view=CreateTicket('Suporte')
            )
        elif self.values[0] == "team_ticket":
            embed = discord.Embed(
                colour=discord.Color.gold(),
                title="Escolha para qual cargo você gostaria de se candidatar",
                description="Escolha uma das opções abaixo para se candidatar ao cargo desejado:"
            )

            embed.add_field(
                name="<:emoji_construct:1194708113077579946> Construtor",
                value="Este cargo é responsável por divulgar eventos e atividades, promovendo e atraindo participantes para as atividades do servidor.",
                inline=False
            )

            embed.add_field(
                name="<:emoji_promoter:1194708133042470933> Promotor",
                value="Este cargo é responsável por divulgar eventos e atividades, promovendo e atraindo participantes para as atividades do servidor.",
                inline=False
            )

            embed.add_field(
                name="<:emoji_programmer:1194707818272534588> Programador",
                value="O cargo de Programador envolve ajudar no desenvolvimento de soluções tecnológicas e ferramentas para o servidor, contribuindo com código e ideias inovadoras.",
                inline=False
            )
            embed.add_field(
                name="<:emoji_content:1194708650946744321> Conteúdo",
                value="A posição de Conteúdo é ideal para aqueles que desejam criar e editar conteúdo, como textos, imagens ou vídeos para os eventos e atividades do servidor.",
                inline=False,
            )

            embed.add_field(
                name="<:emoji_marketing:1194707758700843128> Marketing",
                value="Os membros do cargo de Marketing são responsáveis por criar estratégias de marketing e promoção para aumentar a visibilidade e participação nas atividades do servidor.",
                inline=False
            )
            embed.add_field(
                name="<:emoji_locutor:1194707778015600661> Locutor",
                value="O cargo de Locutor envolve a narração e apresentação de eventos, criando uma atmosfera envolvente para os participantes durante as atividades do servidor.",
                inline=False
            )

            embed.set_image(url="https://github.com/8b1tz/bot_discord/blob/main/app/imgs/wallpaper_support.png?raw=true")
            await interaction.response.send_message(
                ephemeral=True,
                view=TicketButtons(),
                embed=embed,
            )


class CreateTicket(discord.ui.View):
    def __init__(self, ticket_type):
        super().__init__(timeout=300)
        self.value = None,
        self.ticket_type = ticket_type
    
    @discord.ui.button(
        label="Abrir Ticket",
        style=discord.ButtonStyle.blurple,
        emoji="<:ticket:1194712252511699015>")
    async def confirm(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        self.value = True
        self.stop()

        ticket = None
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
                name=f"{self.ticket_type if self.ticket_type else ''} {interaction.user.name} ({interaction.user.id})", 
                auto_archive_duration=10080)
            await ticket.edit(invitable=False)      
        await interaction.response.send_message(ephemeral=True, 
                                                content=f"Criei um ticket para você! {ticket.mention}")
        await ticket.send(f"✉️ **|** {interaction.user.mention} ticket criado! \n\n <@1193661140673245276>")
        


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
    embed.set_image(url="https://github.com/8b1tz/bot_discord/blob/main/app/imgs/wallpaper_ticket.png?raw=true")

    await interaction.channel.send(embed=embed, view=DropdownView())


@tree.command(guild=discord.Object(id=id_server), name="fecharticket", description="Fecha o ticket")
@commands.has_permissions(manage_guild=True)
async def fecharticket(interaction: discord.Interaction):
    mod = interaction.guild.get_role(1193661140673245276)
    try:
        if str(interaction.user.id) in interaction.channel.name or mod in interaction.author.role:
            await interaction.channel.delete()
        else:
            await interaction.response.send_message( "Isso não pode ser feito", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)

class TicketButtons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Promotor",style=discord.ButtonStyle.gray)
    async def promoter(self,
        interaction: discord.Interaction,
        button: discord.ui.Button):
        await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket('Promotor')
            )

    @discord.ui.button(label="Construtor",style=discord.ButtonStyle.gray)
    async def construct(self,
        interaction: discord.Interaction,
        button: discord.ui.Button):
        await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket('Construtor')
            )

    @discord.ui.button(label="Programador",style=discord.ButtonStyle.gray)
    async def programmer(self,
        interaction: discord.Interaction,
        button: discord.ui.Button):
        await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket('Programador')
            )

    @discord.ui.button(label="Marketing",style=discord.ButtonStyle.gray)
    async def marketing(self,
        interaction: discord.Interaction,
        button: discord.ui.Button):
        await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket('Marketing')
            )

    @discord.ui.button(label="Conteúdo",style=discord.ButtonStyle.gray)
    async def content(self,
        interaction: discord.Interaction,
        button: discord.ui.Button):
        await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket('Conteudo')
            )
        
    @discord.ui.button(label="Locutor",style=discord.ButtonStyle.gray)
    async def locuter(self,
        interaction: discord.Interaction,
        button: discord.ui.Button):
        await interaction.response.send_message(
                "O usuário escolheu ticket",
                ephemeral=True,
                view=CreateTicket('Locutor')
            )


@tree.command(guild=discord.Object(id=id_server), name='enable')
async def enable(interaction: discord.Interaction, id_enable: str):
    response = get_enable_by_id_or_api(id_enable)
    await interaction.response.send_message(response, ephemeral=True)


@tree.command(guild=discord.Object(id=id_server), name='handitem')
async def handitem(interaction: discord.Interaction, id_handitem: str):
    response = get_hand_item_by_id_or_api(id_handitem)
    await interaction.response.send_message(response, ephemeral=True)

aclient.run(TOKEN)
