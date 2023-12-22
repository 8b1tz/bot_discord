import asyncio
import io
from difflib import get_close_matches

import httpx
import pandas as pd
from discord import Embed, File, Intents
from discord.ext import commands

external_api_url_handitems = "https://images.habblet.city/leet-asset-bundles/gamedata/habblet_texts.json"

intents = Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

all_handitems = None
handitems_loaded = False

all_enables = None
enables_loaded = False


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
        response = await client.get(external_api_url_handitems)
        if response.status_code == 200:
            data = response.json()
            filtered_data = {key: value for key, value in data.items() 
                             if key.startswith("fx_")}
            all_enables = filtered_data
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
        items_formatted = [f"{name}: {handitem_id}" for name, handitem_id in 
                           all_handitems.items()]
        chunk_size = 50
        chunks = [items_formatted[i:i + chunk_size] for i in 
                  range(0, len(items_formatted), chunk_size)]

        for chunk in chunks:
            formatted_chunk = "```\n" + "\n".join(chunk) + "\n```"
            await ctx.send(formatted_chunk)
    else:
        try:
            if not id.isdigit():
                matching_items = get_close_matches(id.lower(), 
                                                   all_handitems.keys(), n=5, cutoff=0.6)
                if matching_items:
                    matched_results = [f"{all_handitems[name]}: {name}" for name in matching_items]  
                    
                    formatted_result = "\n".join(matched_results)
                    await ctx.send(f"Opções próximas:\n```{formatted_result}```")
                    return

            else:
                handitem_id = int(id)
                for name, item_id in all_handitems.items():
                    if item_id == handitem_id:
                        image_api = f"https://imager.radiohabblet.com.br/?user={user}&action=std,crr={id}&gesture=std&direction=4&head_direction=4&headonly=false&size=b&img_format=&dance=&effect=&frame_num=30"
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
            effects_formatted = []
            for effect_id, effect_name in all_enables.items():
                if not effect_id.endswith('_desc'):
                    effect_desc = all_enables.get(f"{effect_id}_desc", 
                                                  "Descrição não encontrada")
                    formatted_effect = f"{effect_name}: \
                        {effect_id.split('_')[1]}"
                    effects_formatted.append(formatted_effect)

            chunk_size = 10  # Reduzindo o tamanho dos chunks
            chunks = [effects_formatted[i:i + chunk_size] for i in range(0, len(effects_formatted), chunk_size)]

            for chunk in chunks:
                formatted_chunk = "```\n" + "\n".join(chunk) + "\n```"
                await ctx.send(formatted_chunk)
        else:
            effect = f"fx_{effect_id}"
            if effect in all_enables:
                effect_name = all_enables[effect]
                effect_desc = all_enables.get(f"{effect}_desc", "Descrição não encontrada")
                effect_image = f"https://imager.radiohabblet.com.br/?user={user}&action=std,crr=&gesture=std&direction=4&head_direction=4&headonly=false&size=b&img_format=&dance=&effect={effect_id}&frame_num=30"

                async with httpx.AsyncClient() as client:
                    response = await client.get(effect_image)
                    if response.status_code == 200:
                        image_data = response.content
                        image_file = io.BytesIO(image_data)
                        embed = Embed(title=f"**{effect_name} \nID:** {effect_id}", description=effect_desc, color=0x00ff00)
                        embed.set_image(url="attachment://image.png")
                        await ctx.send(file=File(image_file, filename="image.png"), embed=embed)
                    else:
                        await ctx.send(f"**ID:** {effect_id}\n**Nome:** {effect_name}\n**Descrição:** {effect_desc}\n**Imagem:** Imagem não encontrada")
            else:
                await ctx.send("Efeito não encontrado.")
    except ValueError:
        await ctx.send("Por favor, forneça um ID válido para o efeito.")


@bot.command()
async def wired(ctx, wired_type: str = '*'):
    pass


@bot.command()
async def image(ctx, theme: str):
    pass


@bot.command()
async def badge(ctx, id_badge: int = '*'):
    pass


@bot.command()
async def match(ctx, user: str, other_user: str):
    pass


@bot.command()
async def commands(ctx):
    pass


@bot.command()
async def socar(ctx, other_user: str):
    pass


@bot.command()
async def beijar(ctx, other_user: str):
    pass

bot.run('MTE4MzUzMDAyMDI3NTIzNjkyNA.GlE1p-.OdrN51TJybmFu_QMSF3jD61bf1TYV18aLtLGog')
