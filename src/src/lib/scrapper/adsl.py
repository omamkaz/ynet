#!/usr/bin/python3

import re
import requests
from bs4 import BeautifulSoup
from typing import Any, Callable


class Erros:
    @classmethod
    def err(cls, resp: requests.Response) -> str | None:
        '''if the return is None that means doesn't have any error!'''

        soup = ADSL.bs4(resp)

        if "Invalid username or password!" in soup.text.strip():
            return "خطأ في اسم المستخدم أو كلمة مرور!"

        elif (err := soup.find("span", id="ctl00_ContentPlaceHolder1_labErr")) is not None and err.text.strip():
            return "الرمز غير مطابق للصورة، يرجى المحاولة مرة أخرى"

        elif (err := soup.find("span", id="ctl00_ContentPlaceHolder1_LabMsg")) is not None and err.text.strip():
            return err.text


class Payload:
    username: str = "ctl00$ContentPlaceHolder1$loginframe$UserName"
    password: str = "ctl00$ContentPlaceHolder1$loginframe$Password"
    captcha: str = "ctl00$ContentPlaceHolder1$capres"
    login_btn: str = "ctl00$ContentPlaceHolder1$loginframe$LoginButton"
    captcha_btn: str = "ctl00$ContentPlaceHolder1$submitCaptch"
    credit_submit: str = "ctl00$ContentPlaceHolder1$ppSubmit"
    credit_card: str = "ctl00$ContentPlaceHolder1$ppCard" # {1..15}

    login_btn_default: str = "Sign+In"
    captcha_btn_default: str = "Submit"
    credit_submit_default: str = "++++إدراج++++"

    def __init__(self, 
                 username: str = None, 
                 password: str = None,
                 login_btn: str = None):

        self._data = {}
        self._data[Payload.username] = username
        self._data[Payload.password] = password
        self._data[Payload.login_btn] = login_btn or self.login_btn_default

    def set_username(self, username: str) -> None:
        self._data[Payload.username] = username

    def set_password(self, password: str) -> None:
        self._data[Payload.password] = password
    
    def set_login_btn(self, login_btn: str = None) -> None:
        self._data[Payload.login_btn] = login_btn or self.login_btn_default

    def set_login(self, username: str, password: str, login_btn: str = None) -> None:
        self.set_username(username)
        self.set_password(password)
        self.set_login_btn(login_btn or self.login_btn_default)

    def set_captcha(self, captcha: str, captcha_btn: str = None) -> None:
        self._data[Payload.captcha] = captcha
        self._data[Payload.captcha_btn] = captcha_btn or self.captcha_btn_default

    def set_captcha_btn(self, captcha_btn: str = None) -> None:
        self._data[Payload.captcha_btn] = captcha_btn or self.captcha_btn_default

    def set_credit_submit(self, submit: str = None) -> None:
        self._data[Payload.credit_submit] = submit or self.credit_submit_default

    def set_credit_cards(self, cards: list[int | str]) -> None:
        self._data.update(
            {
                Payload.credit_card + str(i): str(card)
                for i, card in enumerate(cards, 1)
            }
        )

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    @property
    def data(self) -> dict:
        return self._data


class ADSL:
    URL = "https://adsl.yemen.net.ye"

    def __init__(
            self, 
            lang: str = "ar", # en|ar
            cookies: dict = None):

        self._lang: str = lang
        self._timeout: int = 10
        self._payload: Payload = Payload()

        self.init_session(cookies)

    @staticmethod
    def bs4(req) -> BeautifulSoup:
        return BeautifulSoup(req.content, "html.parser")

    def init_session(self, cookies: dict = None):
        self._session = requests.Session()
        if cookies is not None:
            self.set_cookies(cookies)

    def fetch_payload_data(self, req: Callable) -> None:
        resp = req()
        resp_soup = self.bs4(resp)
        for _input in resp_soup.find("form", attrs={"name": "aspnetForm"}).find_all("input"):
            if (name := _input.attrs.get("name")).startswith("_"):
                self._payload.set(name, _input.attrs.get("value"))
        return resp

    def login(self, 
              username: str = None, 
              password: str = None) -> int:

        self.clear_cookies()

        if username is not None:
            self._payload.set_username(username)

        if password is not None:
            self._payload.set_password(password)

        # Login GET method
        self.fetch_payload_data(lambda: self._session.get(self._login_url, timeout=self._timeout))

        # Login POST method
        _post = self.fetch_payload_data(lambda: self._session.post(self._login_url, 
                                                                   self._payload.data,
                                                                   allow_redirects=True, 
                                                                   timeout=self._timeout))
        return _post.status_code

    def replace_exception(self, func: Callable) -> Any | None:
        try:
            return func()
        except Exception:
            pass

    def verify(self, captcha: str) -> tuple[requests.Response, str | None]:
        self._payload.set_captcha(captcha)
        resp = self._session.post(self._login_url, data=self._payload.data, timeout=self._timeout)
        return (self.replace_exception(lambda: self.parse_data(resp)), Erros.err(resp))

    def parse_data(self, resp: requests.Response) -> dict[str, str]:
        resp_soup = self.bs4(resp)

        name = resp_soup.find("span", id="ctl00_labWelcome").text.strip()
        labels = resp_soup.find_all("td", class_="td_mc")
        values = resp_soup.find_all("span", attrs={"id": re.compile(r"ctl00_ContentPlaceHolder1_\d+")})

        data = {
            "name": name.split(":")[-1].strip(),
            "account_status": values.pop(2).text.strip() == "حساب نشط",
            "valid_credit": values.pop(-2).text.strip()
        }

        labels.pop(2)
        labels.pop(-2)

        data.update(
            {
                k.text.strip(): v.text.strip()
                for k, v in zip(labels, values)
            }
        )
        return data

    def fetch_data(self, cookies: dict = None) -> dict:
        if cookies is not None:
            self.clear_cookies()
            self.set_cookies(cookies)
        return self.parse_data(self._session.get(self._user_url, timeout=self._timeout))

    def fetch_captcha(self) -> bytes:
        return self._session.get(self._captcha_url).content

    def fetch_credit(self, cards: list[int | str]) -> None:
        self.fetch_payload_data(lambda: self._session.get(self._credit_url, timeout=self._timeout))

        self._payload.set_credit_cards(cards)
        self._payload.set_credit_submit()

        _post = self.fetch_payload_data(lambda: self._session.post(self._credit_url,
                                                                   self._payload.data,
                                                                   allow_redirects=True,
                                                                   timeout=self._timeout))

        return "", Erros.err(_post)

    def get_cookies(self) -> dict:
        return requests.utils.dict_from_cookiejar(self._session.cookies)

    def set_cookies(self, cookies: dict):
        return self._session.cookies.update(requests.utils.cookiejar_from_dict(cookies))

    def export_cookies(self) -> dict:
        return self.get_cookies()

    def import_cookies(self, cookies: dict):
        return self.set_cookies(cookies)

    def clear_cookies(self):
        self._session.cookies.clear()
        self._session.cookies.clear_expired_cookies()

    @property
    def _login_url(self) -> str:
        return f"{self.URL}/{self._lang}/login.aspx"

    @property
    def _user_url(self) -> str:
        return f"{self.URL}/{self._lang}/user_main.aspx"

    @property
    def _captcha_url(self) -> str:
        return f"{self.URL}/captcha/docap.aspx?new=1"

    @property
    def _credit_url(self) -> str:
        return f"{self.URL}/{self._lang}/add-credit.aspx"