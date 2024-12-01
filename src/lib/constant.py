#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import flet as ft
from humanize import naturalsize


APP_VERSION = "v11"
USERNAME = "omamkaz"
ACCOUNT_TYPES = ("الأنترنت المنزلي (ADSL)", "الفورجي", "الهاتف المنزلي")

ABOUT_LINK_ICONS = (
    ("google", "#db4437", f"mailto:{USERNAME}@gmail.com"),
    ("paypal", "#00a7ce", f"PayPal.me/{USERNAME}"),
    ("telegram", "#0088cc", f"https://t.me/{USERNAME}"),
    ("whatsapp", "#25d366", "https://wa.me/967776973923"),
    ("github", "#000000", f"https://www.github.com/{USERNAME}"),
    ("twitter", "#1da1f2", f"https://www.twitter.com/{USERNAME}"),
    ("facebook", "#1877f2", f"https://www.facebook.com/{USERNAME}")
)
THEME_COLORS = (
    "INDIGO", "AMBER", "BLUE", 
    "BROWN", "CYAN", "GREEN", 
    "GREY", "LIME", "ORANGE", 
    "PINK", "PURPLE", "RED", 
    "TEAL", "YELLOW"
)


class Platform:
    @staticmethod
    def is_desktop(page: ft.Page) -> bool:
        return page.platform not in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS)


class Refs:
    cards = ft.Ref[ft.Container]()
    users = ft.Ref[ft.ListView]()


class UserData:

    @staticmethod
    def custom_credit(value: str | float | int) -> str:
        return naturalsize(float(value) * 10**9, format="%.2f")

    @classmethod
    def filter_data(cls, data: dict[str, str], atype: int | str) -> dict[str, str]:
        return getattr(cls, f"type_{atype}")(data)

    @classmethod
    def type_0(cls, data: dict[str, str]) -> dict[str, str]:
        pdata = data.copy()
        for k, v in pdata.items():
            if isinstance(v, str):
                if "جيجابايت" in v:
                    u, _ = v.strip().split()
                    v = UserData.custom_credit(u.strip())
                    data[k] = v
                if "تنبيه" in v:
                    date, warn = v.split("\r")
                    data[k] = date
                    data["تنبية"] = re.sub(r"\*\*(.+)\*\*", "", warn)
        return data

    @classmethod
    def type_1(cls, data: dict[str, str]) -> dict[str, str]:
        for k, v in data.items():
            if "gb" in k.lower():
                u, _ = v.split()
                v = UserData.custom_credit(u.strip())
                data[k] = v
        return data

    @classmethod
    def type_2(cls, data: dict[str, str]) -> dict[str, str]:
        return data


class ThemeController:

    @staticmethod
    def get_theme_mode(page: ft.Page) -> str:
        return (page.client_storage.get("theme_mode")
                or page.platform_brightness.name
                or "system").lower()

    @staticmethod
    def get_theme_color(page: ft.Page) -> str:
        return page.client_storage.get("theme_color") or THEME_COLORS[0]

    @staticmethod
    def get_color(color: str, opacity: int | float) -> str:
        # if color.startswith("#"):
        #     return ft.Colors.with_opacity(0.1, color)
        return color + str(opacity)

    @staticmethod
    def toggle_theme_mode(mode: str, page: ft.Page) -> None:
        page.client_storage.set("theme_mode", mode)
        page.theme_mode = mode
        page.update()

    @staticmethod
    def set_theme_color(color: str, page: ft.Page) -> None:
        color_900 = ThemeController.get_color(color, 900)

        page.theme = page.dark_theme = ft.Theme(
            color_scheme_seed=color,
            use_material3=True,
            font_family="linaround",
            primary_color=color_900,
            divider_theme=ft.DividerTheme(
                color = color_900
            )
        )

        if page.controls:
            controls = page.controls[0].content.controls[0].controls
            controls[0].bgcolor = color

            for c in controls[1].controls[:-1]:
                c.content.bgcolor = ThemeController.get_color(color, 800)

            for t in page.controls[0].content.controls[1].content.controls:
                if t.bgcolor is not None:
                    t.bgcolor = color

        for c in Refs.users.current.controls if Refs.users.current else []:
            c.selected_tile_color = ft.Colors.with_opacity(0.09, color)
        
        page.client_storage.set("theme_color", color)
        page.update()


class Dialogs:

    @staticmethod
    def no_internet_connection(page: ft.Page) -> None:
        page.open(
            ft.AlertDialog(
                icon=ft.Icon(ft.Icons.WIFI_OFF, ft.Colors.RED),
                title=ft.Text(
                    value = "لايوجد اتصال بالأنترنت!",
                    text_align="center",
                    rtl=True
                ),
                content=ft.Lottie(
                    src_base64=LottieFiles.no_internet,
                    fit=ft.ImageFit.COVER
                )
            )
        )

    @staticmethod
    def error(err: str, page: ft.Page) -> None:
        page.open(
            ft.AlertDialog(
                icon=ft.Icon(ft.Icons.ERROR, ft.Colors.RED),
                title=ft.Text(
                    value = str(err),
                    text_align="center",
                    rtl=True
                ),
                content=ft.Lottie(
                    src=LottieFiles.error,
                    fit=ft.ImageFit.COVER
                )
            )
        )


class _LottieFiles:
    def __init__(self):
        files = ("error", "down_arrow", "no_internet", "pin_required", "loading_carga", "online_health_report")
        for name in files:
            self.__setattr__(name, self.lottie_file(name))

    @classmethod
    def lottie_file(cls, name: str) -> str:
        return f"animations/{name}.json"

LottieFiles = _LottieFiles()
