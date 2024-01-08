from httpx import Client, Response


class BaseHabbletApi:
    def __init__(self) -> None:
        self._client = Client()

    def _get(self, url: str) -> Response:
        return self._client.get(url=url)

    def __del__(self) -> None:
        self._client.close()
