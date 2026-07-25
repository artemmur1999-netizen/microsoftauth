import msal
import webview
from urllib.parse import urlparse, parse_qs

def print(*args, **kwargs):
    pass

class MicrosoftAuthCore:

    accounts = {
        "all": "common",
        "work": "organizations",
        "personal": "consumers"
    }

    def __init__(
        self,
        client_id,
        scopes=None,
        account_type="all",
        custom_id=None
    ):

        self.client_id = client_id

        self.scopes = scopes or [
            "User.Read"
        ]

        if custom_id:
            self.account_type = custom_id
        else:
            self.account_type = self.accounts.get(
                account_type,
                "common"
            )

        self.redirect = "http://localhost"

        self.authority = (
            "https://login.microsoftonline.com/"
            + self.account_type
        )

        self.msal_app = msal.PublicClientApplication(
            self.client_id,
            authority=self.authority
        )

    def login_data(self):

        return self.msal_app.initiate_auth_code_flow(
            scopes=self.scopes,
            redirect_uri=self.redirect
        )

    def acquire_token(
        self,
        response_url,
        login_data
    ):

        parsed_url = urlparse(response_url)

        query = parse_qs(
            parsed_url.query
        )

        auth_response = {
            key: value[0]
            for key, value in query.items()
        }

        return self.msal_app.acquire_token_by_auth_code_flow(
            login_data,
            auth_response
        )


class MicrosoftAuth:

    def __init__(
        self,
        client_id,
        scopes=None,
        account_type="all",
        custom=None
    ):

        self.main = MicrosoftAuthCore(
            client_id=client_id,
            scopes=scopes or [
                "User.Read"
            ],
            account_type=account_type,
            custom_id=custom
        )

        self.login_data = self.main.login_data()

        self.url = self.login_data["auth_uri"]

        self.result = {}

        self.window = None

        self.finished = False

    def check_url(self):

        if self.finished:
            return

        try:

            url = self.window.get_current_url()

            print(
                "Current URL:",
                url
            )

            if not url:
                return

            if not url.startswith(
                self.main.redirect
            ):
                return

            print(
                "Redirect detected!"
            )

            self.finished = True

            self.result = (
                self.main.acquire_token(
                    url,
                    self.login_data
                )
            )

            print(
                "Authentication completed!"
            )

            self.window.destroy()

        except Exception as e:

            print(
                "AUTH ERROR:",
                repr(e)
            )

            self.result = {
                "error": str(e)
            }

            self.finished = True

            if self.window:

                self.window.destroy()

    def get(self):

        self.window = webview.create_window(
            title="Microsoft Auth",
            url=self.url,
            width=430,
            height=650,
            resizable=False
        )

        self.window.events.loaded += (
            self.check_url
        )

        webview.start()

        return self.result


__VER__ = "1.0.4"