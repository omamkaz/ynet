#!/usr/bin/python3

import requests

from .base import Base, ParserError


class LTE(Base):
    def __init__(self):
        super().__init__()

        self.set_login_url("9017")
        self.set_captcha_url("quarybillcbs-api-plug")

        self._payload.username = "phoneidnew"
        self._payload.captcha = "captcha_code_qbillnew"

        self._payload.set("_wp_http_referer", "/?page_id=9017")
        self._payload.set("doqbillnew", "querybillvaluenew")
        self._payload.set("querybillnew_field", "680d4e17f8")
        self._payload.set("qsubmitnew", "استعلام")

    def verify(self, captcha: str) -> tuple[dict[str, str], str | None]:
        return super().verify(captcha, "phoneidrrornew")

    def translator(self, key: str) -> str:
        return key.replace("Unlimited Min", "غير محدود")

    def login(self, username: str) -> None:
        resp = super().login(username)
        soup = self.bs4(resp)

        value = soup.find("input", id="querybillnew_field").attrs.get("value")
        self._payload.set("querybillnew_field", value)

    def fetch_data(self, resp: requests.Response) -> dict:
        super().fetch_data(resp)

        try:
            resp_soup = self.bs4(resp)
            table = list(resp_soup.find("table", class_="transdetail").find_all("tr"))
            label1 = table[4].find("td").text.strip()

            data = {}
            for tr in table[5:7]:
                key = tr.find("th").text.replace("الرصيد", "").strip()
                data[label1 + f" ({key})"] = self.translator(
                    tr.find("span").text.strip()
                )

            data["valid_credit"] = table[-2].find("td").text.strip()
            data[table[-1].find("th").text.strip()] = self.translator(
                table[-1].find("span").text.strip()
            )

            table.pop(0)
            table.pop(1)

            data.update(
                {
                    tr.find("th").text.strip(): self.translator(
                        tr.find("span").text.strip()
                    )
                    for tr in table[:2]
                }
            )
            return data
        except AttributeError:
            raise ParserError(ParserError.limit_or_service_err())
