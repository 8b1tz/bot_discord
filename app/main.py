from database import Base, SessionLocal, engine
from discord import Embed, File, Intents
from discord.ext import commands
from models import Enable, Handitem, User, UserBadge, UserGroup, UserRoom
from view import UserView

Base.metadata.create_all(
    bind=engine, tables=[
        'enable',
        'handitem',
        'user',
        'friendship',
        'badge',
        'user_badge',
        'room',
        'user_room',
        'groups',
        'user_groups'
        ], checkfirst=True
)

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def user(ctx, name: str) -> None:
    """
    Necessário fazer o profile primeiro e mostrar 
    os botões de sugestão do que o usuário pode escolher
    """
    pass


@bot.command()
async def enable(ctx, id: int = 0, name: str = '') -> None:
    pass


@bot.command()
async def hand(ctx, id: int = 0, name: str = '') -> None:
    pass
