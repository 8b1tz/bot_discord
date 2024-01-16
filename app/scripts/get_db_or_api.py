from habblet_api import HabbletApi
from models import Badge, Enable, Handitem
from repository import (
    get_badge_by_id,
    get_enable_by_id,
    get_handitem_by_id,
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


def get_badge_by_id_or_api(badge_id: str):
    badge = get_badge_by_id(badge_id=badge_id)
    if badge:
        return badge

    hb = HabbletApi()
    list_badge = hb.get_badges()
    filtered_badge = list(filter(lambda x: str(x["id"]) == badge_id, list_badge))[0]
    if filtered_badge:
        badge = Badge(id=filtered_badge["id"], name=filtered_badge["name"])
        return badge
    return f"O badge com o id {badge_id} não foi encontrado."
