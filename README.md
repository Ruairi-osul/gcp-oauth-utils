# GCP OAuth Utils

This is a small Python library for working with the OAuth2 protocol on Google Cloud Platform.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```sh
pip install git+https://github.com/Ruairi-osul/gcp-oauth-utils.git
```

## Usage
The library provides one main class: `GCPAuthenticator`.

#### GCPAuthenticator
The GCPAuthenticator class is takes a path to a credentials `json` file, a set of scopes and a path to a token `json` which does not need to exist.

The main method is `get_token` which will return a token. If the token does not exist or is expired, it will be refreshed. If the token is not refreshable, a new one will be requested.

The `get_token` method will also save the token to the token path if it does not exist or is expired.

```python
from gcp_oauth_utils import GCPAuthenticator

authenticator = GCPAuthenticator(scopes, oauth_creds_path, token_path)

# saves token to token_path
token = authenticator.get_token()

# to force a refresh
token = authenticator.get_token(force_refresh=True)

# to force regeneration of token
token = authenticator.get_token(force_generate=True)
```
