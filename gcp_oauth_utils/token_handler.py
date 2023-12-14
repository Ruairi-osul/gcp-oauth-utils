from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pathlib import Path

class TokenHandler:
    def __init__(self, token_path: str | Path):
        self.token_path = Path(token_path)
        self._token: Credentials | None = None

    @property
    def exists(self) -> bool:
        return self.token_path.exists()

    @property
    def token(self) -> Credentials:
        if self._token is None:
            self._token = Credentials.from_authorized_user_file(self.token_path)
        return self._token

    @property
    def is_expired(self) -> bool:
        return self.token.expired

    @property
    def is_valid(self) -> bool:
        return self.token.valid

    @property
    def is_refreshable(self) -> bool:
        return self.token.refresh_token is not None

    def refresh(self) -> None:
        if self.is_refreshable:
            self.token.refresh(Request())
            self._reinstantiate_token()
        else:
            raise ValueError("Cannot refresh credentials. Refresh token is None.")

    def _reinstantiate_token(self) -> None:
        self._token = Credentials.from_authorized_user_file(self.token_path)
