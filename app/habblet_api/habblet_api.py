import re

from .base_api import BaseHabbletApi


class HabbletApi(BaseHabbletApi):
    def __init__(self) -> None:
        super().__init__()

    def get_user_by_name(self, name: str) -> dict:
        api_url = f"https://www.habblet.city/api/player/{name}"
        response = self._get(api_url)

        if response.status_code == 200:
            return response.json()

        raise Exception(
            f"Falha na requisição para API: {api_url}. "
            f"Status Code: {response.status_code}"
        )

    def get_handitem(self) -> list:
        api_url = (
            "https://images.habblet.city/leet-asset-bundles/gamedata/habblet_texts.json"
        )

        response = self._get(api_url)

        if response.status_code == 200:
            pattern = re.compile(r"handitem\d+")
            dados = response.json()
            return {
                int(re.search(r"\d+", chave).group()): valor
                for chave, valor in dados.items()
                if pattern.match(chave)
            }
        #     data = response.json()

    def get_enables(self) -> list:
        api_url = (
            "https://images.habblet.city/leet-asset-bundles/gamedata/"
            "avatar/EffectMap.json?v=109"
        )
        response = self._get(api_url)
        enables_list = []

        if response.status_code == 200:
            data = response.json()
            enables_data = data.get("effects", [])

            fx_enables_data = filter(lambda x: x.get("type") == "fx", enables_data)

            enables_list.extend(
                {"id": enable_data.get("id"), "name": enable_data.get("lib")}
                for enable_data in fx_enables_data
            )
            return enables_list

        raise Exception(
            f"Falha na requisição para API: {api_url}. "
            f"Status Code: {response.status_code}"
        )

    def get_badge_by_id(self, id: int):
        pass

    def get_new_badge_in_game(self):
        pass
