from models import Enable, Handitem
from repository import get_enable_by_id


class HabbletApi:
    
    def get_user_by_name(self, name):
        pass

    def get_handitem_id(self, id: int = 0) -> list[Handitem]:
        pass
        # api_url = "https://images.habblet.city/leet-asset-bundles/gamedata/\
        # habblet_texts.json"
        # response = self.get(api_url)
        # handitem_list = []
        # if response.status == 200:
        #     data = response.json()

    def get_enables_id(self, id: int = 0) -> list[Enable]:

        enable_result = get_enable_by_id(enable_id=id)

        if enable_result:
            return enable_result

        api_url = "https://images.habblet.city/leet-asset-bundles/gamedata/\
        avatar/EffectMap.json?v=109"
        response = self.get(api_url)
        enables_list = []

        if response.status_code == 200:
            data = response.json()
            enables_data = data.get("effects", [])

            fx_enables_data = filter(
                lambda x: x.get("type") == "fx",
                enables_data
            )

            enables_list.extend(
                Enable(
                    id=enable_data.get("id"),
                    name=enable_data.get("lib")
                )
                for enable_data in fx_enables_data
            )

        else:
            raise Exception(
                f"Falha na requisição para API: {api_url}. "
                f"Status Code: {response.status_code}"
            )

        return enables_list
    
    def get_badge_by_id(self, id: int):
        pass

    def get_new_badge_in_game(self):
        pass