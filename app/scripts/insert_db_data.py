from habblet_api import HabbletApi
from models import Enable, Handitem
from repository import insert_enable, insert_handitem
from sqlalchemy.exc import IntegrityError


def init_db_data():
    hb = HabbletApi()

    list_enables = hb.get_enables()
    for enable in list_enables:
        try:
            obj_enable = Enable(id=enable["id"], name=enable["name"])
            insert_enable(enable=obj_enable)
        except IntegrityError:
            pass

    list_hand_items = hb.get_handitem()
    for hand_item in list_hand_items:
        try:
            obj_hand_item = Handitem(id=hand_item["id"], name=hand_item["name"])
            insert_handitem(handitem=obj_hand_item)
        except IntegrityError:
            pass
