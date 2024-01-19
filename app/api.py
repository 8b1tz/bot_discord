from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Enable, Handitem
from scripts import get_enable_by_id_or_api, get_hand_item_by_id_or_api

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/enable/{id}")
async def get_enable_by_id(id: int) -> Enable:
    enable = get_enable_by_id_or_api(id)
    return enable


@app.get("/handitem/{id}")
async def get_handitem_by_id(id: int) -> Handitem:
    handitem = get_hand_item_by_id_or_api(id)
    return handitem


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=7070)
