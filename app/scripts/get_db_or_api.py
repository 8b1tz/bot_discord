from habblet_api import HabbletApi
from models import Enable, Handitem
from repository import get_enable_by_id, get_handitem, insert_enable, insert_handitem


def get_enable_by_id_or_api(enable_id: int):
    enable = get_enable_by_id(enable_id=enable_id)
    if enable:
        return enable
    hb = HabbletApi()
    list_enables = hb.get_enables()

    filtered_enable = list(filter(lambda x: x["id"] == enable_id, list_enables))
    if filtered_enable:
        enable = Enable(id=filtered_enable[0]["id"], name=filtered_enable[0]["name"])
        insert_enable(enable=enable)
        return enable
    return f"Enable de id: {enable_id} não existe."


def get_hand_item_by_id_or_api(hand_item_id: int):
    hand_item = get_handitem(hand_item_id=hand_item_id)
    if hand_item:
        return hand_item
    hb = HabbletApi()
    list_hand_item = hb.get_handitem()

    filtered_enable = list(filter(lambda x: x["id"] == hand_item_id, list_hand_item))
    if filtered_enable:
        hand_item = Handitem(
            id=filtered_enable[0]["id"], name=filtered_enable[0]["name"]
        )
        insert_handitem(handitem=hand_item)
        return hand_item
    return f"HandItem de id: {hand_item_id} não existe."
