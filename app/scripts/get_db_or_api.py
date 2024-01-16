from habblet_api import HabbletApi
from models import Enable, Handitem, Badge
from repository import (
    get_enable_by_id,
    get_handitem_by_id,
    get_wired_by_id,
    insert_enable,
    insert_handitem,
)


def get_enable_by_id_or_api(enable_id: str):
    enable = get_enable_by_id(enable_id=enable_id)
    if enable:
        return enable
    hb = HabbletApi()
    list_enables = hb.get_enables()
    filtered_enable = list(filter(lambda x: str(x["id"]) == enable_id, list_enables))
    if filtered_enable:
        enable = Enable(id=filtered_enable[0]["id"], name=filtered_enable[0]["name"])
        insert_enable(enable=enable)
        return enable
    return f"O enable com o id {enable_id} não foi encontrado."


def get_hand_item_by_id_or_api(hand_item_id: str):
    hand_item = get_handitem_by_id(handitem_id=hand_item_id)
    if hand_item:
        return hand_item
    hb = HabbletApi()
    list_hand_item = hb.get_handitem()
    filtered_enable = list(
        filter(lambda x: str(x["id"]) == hand_item_id, list_hand_item)
    )
    if filtered_enable:
        hand_item = Handitem(
            id=filtered_enable[0]["id"], name=filtered_enable[0]["name"]
        )
        insert_handitem(handitem=hand_item)
        return hand_item
    return f"O enable com o id {hand_item_id} não foi encontrado."


def get_enable_by_id_or_api(enable_id: str):
    enable = get_enable_by_id(enable_id=enable_id)
    if enable:
        return enable

    hb = HabbletApi()
    list_enable = hb.get_badges()
    filtered_enable = list(filter(lambda x: str(x["id"]) == enable_id, list_enable))
    if filtered_enable:
        enable = Badge(id=)
