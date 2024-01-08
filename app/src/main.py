import asyncio
import io
import os
from difflib import get_close_matches

import httpx
import interactions
import pandas as pd
from discord import ButtonStyle, Color, Embed, File, Intents
from discord.ext import commands
from PIL import Image

external_api_url_handitems = "https://images.habblet.city/leet-asset-bundles/gamedata/habblet_texts.json"

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

all_handitems = None
handitems_loaded = False

all_enables = None
enables_loaded = False

async def send_chunks(ctx, data, chunk_size, title):
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    for chunk in chunks:
        formatted_chunk = "```\n" + "\n".join(chunk) + "\n```"
        embed = Embed(title=title, description=formatted_chunk, color=Color.green())
        await ctx.send(embed=embed)


async def fetch_all_handitems():
    global all_handitems, handitems_loaded
    async with httpx.AsyncClient() as client:
        response = await client.get(external_api_url_handitems)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data.items(), columns=["key", "value"])
            filtered_df = df[df["key"].str.match(r'handitem\d+')]
            extracted_data = {
                row["value"]: int(row["key"].split("handitem")[1])
                for _, row in filtered_df.iterrows()
            }
            all_handitems = extracted_data
            handitems_loaded = True
        else:
            all_handitems = None
            handitems_loaded = False


async def fetch_all_enables():
    global all_enables, enables_loaded
    async with httpx.AsyncClient() as client:
        response = await client.get("https://images.habblet.city/leet-asset-bundles/gamedata/avatar/EffectMap.json?v=109")
        if response.status_code == 200:
            data = response.json()
            all_enables = {effect["id"]: effect["lib"] for effect in data.get("effects", [])}
            enables_loaded = True
        else:
            all_enables = None
            enables_loaded = False


@bot.event
async def on_ready():
    await fetch_all_handitems()
    await fetch_all_enables()
    print("Handitems e Efeitos carregados com sucesso.")


async def wait_for_data(ctx):
    while not handitems_loaded or not enables_loaded:
        await asyncio.sleep(1)


@bot.command()
async def hand(ctx, id: str = '*'):
    await wait_for_data(ctx)
    global all_handitems
    user = ctx.author.display_name
    if id == "*":
        items_formatted = [f"{name}: {handitem_id}" for name, handitem_id in all_handitems.items()]
        chunk_size = 50
        await send_chunks(ctx, items_formatted, chunk_size, "Handitems")
    else:
        try:
            if not id.isdigit():
                matching_items = get_close_matches(id.lower(), all_handitems.keys(), n=5, cutoff=0.6)
                if matching_items:
                    matched_results = [f"{all_handitems[name]}: {name}" for name in matching_items]
                    formatted_result = "\n".join(matched_results)
                    await ctx.send(f"Opções próximas:\n```{formatted_result}```")
                    return
            else:
                handitem_id = int(id)
                for name, item_id in all_handitems.items():
                    if item_id == handitem_id:
                        image_api = f"https://www.habbonce.site/api/imagens?nick={user}&action=std,crr={id}&gesture=std&direction=4&head_direction=4&headonly=false&size=b&img_format=&dance=&effect=&frame_num=30"
                        async with httpx.AsyncClient() as client:
                            image_response = await client.get(image_api)
                            image_data = image_response.content
                        if image_response.status_code == 200:
                            image_file = io.BytesIO(image_data)
                            embed = Embed(title=f"**{name} \nID:** {handitem_id}", description="Veja o item abaixo:", color=0x00ff00)
                            embed.set_image(url="attachment://image.png")
                            await ctx.send(file=File(image_file, filename="image.png"), embed=embed)
                        else:
                            message = f"**{name}: {handitem_id}**"
                            await ctx.send(message)
                        return
            await ctx.send("Handitem não encontrado.")
        except ValueError:
            await ctx.send("Por favor, forneça um ID válido para o handitem.")



@bot.command()
async def enable(ctx, effect_id: str = '*'):
    await wait_for_data(ctx)
    global all_enables
    user = ctx.author.display_name

    try:
        if effect_id == '*':
            effects_formatted = [f"NOME: {effect_name}: {effect_id}" for effect_id, effect_name in all_enables.items()]
            chunk_size = 10
            await send_chunks(ctx, effects_formatted, chunk_size, "Efeitos")
        else:
            if effect_id in all_enables:
                effect_name = all_enables[effect_id]
                effect_image_api = f"https://imager.radiohabblet.com.br/?user={user}&action=std,crr=&gesture=std&direction=4&head_direction=4&headonly=false&size=b&img_format=&dance=&effect={effect_id}&frame_num=30"
                async with httpx.AsyncClient() as client:
                    effect_image_response = await client.get(effect_image_api)
                    effect_image_data = effect_image_response.content

                if effect_image_response.status_code == 200:
                    effect_image_file = io.BytesIO(effect_image_data)
                    embed = Embed(title=f"**{effect_name} \nID:** {effect_id}", description="Veja o efeito abaixo:", color=0x00ff00)
                    embed.set_image(url="attachment://image.png")

                    await ctx.send(file=File(effect_image_file, filename="image.png"), embed=embed)
                else:
                    message = f"**{effect_name}: {effect_id}**"
                    await ctx.send(message)
            else:
                await ctx.send("Efeito não encontrado.")
    except ValueError:
        await ctx.send("Por favor, forneça um ID válido para o efeito.")


@bot.command()
async def wired(ctx, wired_type: str = '*'):
    pass


@bot.command()
async def image(ctx, user: str, theme: str):
    image_folder = 'imgs'
    theme_image_path = os.path.join(image_folder, f"{theme}.png")
    if not os.path.exists(theme_image_path):
        await ctx.send(f"Imagem para o tema '{theme}' não encontrada.")
        return
    user_image_url = f"https://www.habbonce.site/api/imagens?nick={user}&action=std,crr=50&head_direction=3&direction=4"
    async with httpx.AsyncClient() as client:
        response = await client.get(user_image_url)
        if response.status_code == 200:
            user_image = Image.open(io.BytesIO(response.content))
            theme_image = Image.open(theme_image_path)
            user_image = user_image.resize((1000, 1200))
            x_offset = 250
            y_offset = -20
            theme_image.paste(user_image, (x_offset, y_offset), user_image)
            with io.BytesIO() as image_binary:
                theme_image.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=File(image_binary, filename='combined_image.png'))
        else:
            await ctx.send("Falha ao obter a imagem do usuário.")


async def get_user_info(ctx, user, endpoint_key, result_key):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.habblet.city/api/player/{user}/{endpoint_key}")

    if response.status_code == 200:
        data = response.json()
        result_data = data if not result_key else [item[result_key] for item in data]
        chunk_size = 10
        await send_chunks(ctx, result_data, chunk_size, f"Informações do usuário {user}: {endpoint_key.capitalize()}")
    else:
        await ctx.send(f"Erro ao obter informações de {endpoint_key} do usuário.")


async def get_user_badge_info(ctx, user):
    await get_user_info(ctx, user, "badges", None)


async def get_user_groups_info(ctx, user):
    await get_user_info(ctx, user, "groups", "name")


async def get_user_rooms_info(ctx, user):
    await get_user_info(ctx, user, "rooms", "name")

async def get_user_friends_info(ctx, user):
    await get_user_info(ctx, user, "friends", "username")



@bot.command()
async def user(ctx, username: str):

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.habblet.city/api/player/{user}") # noqa

    if response.status_code == 200:
        data = response.json()
        await ctx.send(data)
    else:
        await ctx.send(f"Erro ao obter informações de {username}")

    action_row = [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": ButtonStyle.blue,
                    "label": "AMIGOS",
                    "custom_id": "friends"
                },
                {
                    "type": 2,
                    "style": ButtonStyle.blue,
                    "label": "EMBLEMAS",
                    "custom_id": "badges"
                },
                {
                    "type": 2,
                    "style": ButtonStyle.blue,
                    "label": "GRUPOS",
                    "custom_id": "groups"
                },
                {
                    "type": 2,
                    "style": ButtonStyle.blue,
                    "label": "ROOMS",
                    "custom_id": "rooms"
                }
            ]
        }
    ]

    await ctx.send(
        f"Escolha uma opção para o usuário {username}:",
        components=action_row
    )

@bot.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "friends":
        await interaction.response.send_message(content="Aqui estão os amigos do usuário.", ephemeral=True) # noqa
    elif interaction.component.custom_id == "badges":
        await interaction.response.send_message(content="Aqui estão os emblemas do usuário.", ephemeral=True) # noqa
    elif interaction.component.custom_id == "groups":
        await interaction.response.send_message(content="Aqui estão os grupos do usuário.", ephemeral=True) # noqa
    elif interaction.component.custom_id == "rooms":
        await interaction.response.send_message(content="Aqui estão os quartos do usuário.", ephemeral=True) # noqa
 

bot.run('MTE4MzUzMDAyMDI3NTIzNjkyNA.GlE1p-.OdrN51TJybmFu_QMSF3jD61bf1TYV18aLtLGog') # noqa
