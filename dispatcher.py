import requests
import exceptions
from requests.adapters import HTTPAdapter
from urllib3 import Timeout
from urllib3.util.retry import Retry


class Dispatcher:

    def __init__(self, data):
        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.sp_dc = data['sp_dc']
        self.discord_token = data['discord_token']

    async def get_current_playing_track(self, access_token):
        track = self.session.get("https://api.spotify.com/v1/me/player/currently-playing",
                                 headers={
                                     "Accept": "application/json",
                                     "Content-Type": "application/json",
                                     "Authorization": f"Bearer {access_token}"}, timeout=Timeout(connect=2, read=60)
                                 )
        if track.status_code == 200:
            return track
        elif track.status_code == 401:
            raise exceptions.AccessTokenExpired(track)
        else:
            return None

    async def get_access_token(self):
        req = self.session.get("https://open.spotify.com/get_access_token?reason=transport&productType=web-player",
                               headers={"accept": "application/json",
                                        "accept-language": "ru",
                                        "app-platform": "WebPlayer",
                                        "cache-control": "no-cache",
                                        "pragma": "no-cache",
                                        "sec-fetch-dest": "empty",
                                        "sec-fetch-mode": "cors",
                                        "sec-fetch-site": "same-origin",
                                        "spotify-app-version": "1.1.96.83.g8ad99f81",
                                        "cookie": f"sp_dc={self.sp_dc}",
                                        "Referer": "https://open.spotify.com/album/4c8PkfUv6QLHkFPEqH0yDw",
                                        "Referrer-Policy": "strict-origin-when-cross-origin"}
                               )
        return {'token': req.json()['accessToken'], "id": req.json()['clientId'],
                "time": req.json()['accessTokenExpirationTimestampMs']}

    async def get_client_token(self, client_id):
        req = self.session.post("https://clienttoken.spotify.com/v1/clienttoken",
                                headers={
                                    "accept": "application/json",
                                    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                                    "cache-control": "no-cache",
                                    "content-type": "application/json",
                                    "pragma": "no-cache",
                                    "sec-fetch-dest": "empty",
                                    "sec-fetch-mode": "cors",
                                    "sec-fetch-site": "same-site",
                                    "Referer": "https://open.spotify.com/",
                                    "Referrer-Policy": "strict-origin-when-cross-origin"
                                },
                                data="{\"client_data\":{\"client_version\":\"1.1.96.83.g8ad99f81\","
                                     "\"client_id\":\"" + client_id + "\",\"js_sdk_data\":{"
                                                                      "\"device_brand\":\"unknown\","
                                                                      "\"device_model\":\"desktop\","
                                                                      "\"os\":\"Windows\", "
                                                                      "\"os_version\":\"NT 10.0\"}}}",
                                )

        return req.json()['granted_token']['token']

    async def get_lyric_request(self, access_token, client_token, track_id):
        req = self.session.get(
            f"https://spclient.wg.spotify.com/color-lyrics/v2/track/{track_id}?format=json&vocalRemoval=false&market=from_token",
            headers={"accept": "application/json",
                     "accept-language": "ru",
                     "app-platform": "WebPlayer",
                     "authorization": f"Bearer {access_token}",
                     "cache-control": "no-cache",
                     "client-token": client_token,
                     "pragma": "no-cache",
                     "sec-fetch-dest": "empty",
                     "sec-fetch-mode": "cors",
                     "sec-fetch-site": "same-site",
                     "spotify-app-version": "1.1.95.549.g44689ec7",
                     "Referer": "https://open.spotify.com/",
                     "Referrer-Policy": "strict-origin-when-cross-origin"}
        )
        return req

    async def send_status(self, text="", emoji=""):
        self.session.patch("https://discord.com/api/v9/users/@me/settings",
                           headers={"authorization": self.discord_token, "content-type": "application/json"},
                           json={"custom_status": {"text": text, "emoji_name": emoji, "timeout": 2900}})
