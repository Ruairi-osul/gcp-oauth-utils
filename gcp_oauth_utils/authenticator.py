from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from .token_handler import TokenHandler


class GCPAuthenticator:
    """
    Authenticates with Google Cloud Platform using OAuth2.0

    Args:
        scopes (list[str]): List of scopes to request access to.
        oauth_creds_path (str | Path): Path to the OAuth2.0 credentials file.
        token_path (str | Path): Path to the token file.

    Methods:
        generate_token: Generates a new token.
        get_existing_token: Gets an existing token.
        refresh_token: Refreshes the token.
        get_token: Gets a token. If no token exists, generates a new one. If token is expired, generates a new one. If token is refreshable, refreshes the token.

    """

    def __init__(
        self, scopes: list[str], oauth_creds_path: str | Path, token_path: str | Path
    ) -> None:
        self.scopes = scopes
        self.oauth_creds_path = Path(oauth_creds_path)
        self.token_path = Path(token_path)
        self.token_handler = TokenHandler(self.token_path)

    def generate_token(self) -> TokenHandler:
        """
        Generates a new token using the oauth_creds_path and scopes attributes.

        Returns:
            TokenHandler: TokenHandler object.
        """
        flow = InstalledAppFlow.from_client_secrets_file(
            self.oauth_creds_path, self.scopes
        )
        token_response = flow.run_local_server(port=0)
        with self.token_path.open("w") as token_file:
            token_file.write(token_response.to_json())
        self.token_handler = TokenHandler(self.token_path)
        return self.token_handler

    def get_existing_token(self) -> TokenHandler:
        """
        Gets an existing token.

        Returns:
            TokenHandler: TokenHandler object.

        Raises:
            ValueError: If token does not exist.
        """
        if not self.token_handler.exists:
            raise ValueError("Cannot get existing token. Token does not exist.")
        return self.token_handler

    def refresh_token(self) -> TokenHandler:
        """
        Refreshes the token.

        Returns:
            TokenHandler: TokenHandler object.

        Raises:
            ValueError: If token is not refreshable.
        """

        if not self.token_handler.is_refreshable:
            raise ValueError("Cannot refresh credentials. Refresh token is None.")
        self.token_handler.refresh()
        return self.token_handler

    def get_token(
        self, force_generate: bool = False, force_refresh: bool = False
    ) -> Credentials:
        """
        Gets a token.
            - If no token exists or is expired and non-refreshable, generates a new one.
            - If token is expired and is refreshable, freshes the token.
            - If the token already exists and is valid, returns the token.

        Args:
            force_generate (bool, optional): Forces generation of a new token. Defaults to False.
            force_refresh (bool, optional): Forces refresh of the token. Defaults to False.

        Returns:
            Credentials: Credentials object.
        """
        if force_generate:
            token_handler = self.generate_token()
        elif not self.token_handler.exists:
            token_handler = self.generate_token()
        elif not self.token_handler.is_valid:
            token_handler = self.generate_token()
        elif self.token_handler.is_expired and not self.token_handler.is_refreshable:
            token_handler = self.generate_token()
        elif self.token_handler.is_expired and self.token_handler.is_refreshable:
            token_handler = self.refresh_token()
        elif force_refresh:
            token_handler = self.refresh_token()
        elif self.token_handler.exists:
            token_handler = self.get_existing_token()
        else:
            token_handler = self.generate_token()

        return token_handler.token
