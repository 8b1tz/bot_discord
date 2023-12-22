import httpx
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()

external_api_url = "https://images.habblet.city/leet-asset-bundles/gamedata/habblet_texts.json"


async def fetch_handitems():
    async with httpx.AsyncClient() as client:
        response = await client.get(external_api_url)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data.items(), columns=["key", "value"])
            filtered_df = df[df["key"].str.match(r'handitem\d+')]
            extracted_data = {
                row["value"]: int(row["key"].split("handitem")[1])
                for _, row in filtered_df.iterrows()
            }
            return extracted_data
        else:
            raise HTTPException(status_code=response.status_code, detail="Handitems not found")


@app.get("/handitems/")
async def get_handitems():
    return await fetch_handitems()


@app.get("/handitem/{id}")
async def get_handitem_by_id(id: int):
    handitems = await fetch_handitems()
    for name, handitem_id in handitems.items():
        if handitem_id == id:
            return {name: handitem_id}
    raise HTTPException(status_code=404, detail="Handitem not found")

