#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests

from .item import CardItem
from .title import CardTitle
from .credit import CardCredit
from ...models.user import User
from ...constant import ThemeController, Refs, Dialogs, Platform
 

class Card(ft.GestureDetector):
    _user_id: int = None
    _isp = None

    def __init__(self, page: ft.Page, atype: int | str = 0, **kwargs):
        super().__init__(**kwargs)

        self.page = page

        self.card_title: CardTitle = CardTitle(page, atype)
        self.card_credit: CardCredit = CardCredit()
        self.card_items = ft.Ref[ft.Column]()

        self.on_pan_end = self._on_pan_end
        self.on_pan_update = self._on_pan_update

        self.content = ft.Container(
                expand=True,
                padding=0,
                border_radius=16,
                height=self.card_height,
                alignment=ft.alignment.center,
                margin=ft.margin.only(left=14, right=14, top=25),
                animate=ft.Animation(200, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
                bgcolor=ThemeController.get_color(self.page.theme.color_scheme_seed, 800),
                shadow=ft.BoxShadow(
                    spread_radius=-10,
                    blur_radius=8,
                    color=ft.Colors.with_opacity(0.07, ft.Colors.BLACK),
                    offset=ft.Offset(0, 8)
                ),
                content = ft.Column(
                    spacing=0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        self.card_title,
                        self.card_credit,
                        ft.Column(
                            ref=self.card_items,
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    ]
                )
            )

        self.card_title.content.controls[0].controls[0].on_click = lambda e: self._on_pan_end()

    def set_card_items(self, data: dict[str, str]) -> None:
        self.card_items.current.controls.clear()
        self.card_items.current.controls.extend(
            CardItem(label, value, end=(index == len(data) - 1))
            for index, (label, value) in enumerate(data.items())
        )
        self.content.height = self.card_height + (20 * (len(data) - 5)) if len(data) >= 6 else self.card_height

    def set_data(self, user_id: int) -> None:
        self._user_id = user_id

        if not self._user.data:
            Refs.cards.current.toggle_card(4)
            return

        Refs.cards.current.toggle_card(self._user.atype)
        self.set_card_data()

    def set_login(self, user_id: int) -> None:
        self._user_id = user_id

        self.set_loading(True)

        try:
            self.login_web()
        except AttributeError:
            self.start_captcha_verify()
        except requests.exceptions.Timeout:
            Dialogs.connection_timeout(self.page)
        except requests.exceptions.ConnectionError:
            Dialogs.no_internet_connection(self.page)
        except Exception as err:
            Dialogs.error(err, self.page)

        self.set_loading(False)

    def on_captcha_verify_submit(
            self,
            atype: int,
            data: dict[str, str],
            old_data: dict[str, str] = None,
            cookies: dict[str, str] = None) -> None:

        User.edit_data_and_cookies(self._user_id, data, cookies)
        self.set_card_data(old_data)

        Refs.cards.current.toggle_card(atype)
        for c in Refs.users.current.controls:
            c.selected = (self._user_id == c.data)
            c.set_verified(User.get_user(c.data).data is not None)

        Refs.users.current.update()

        # Captcha verify time
        from datetime import datetime
        print("Now: ", datetime.now().timestamp())

    def _on_pan_update(self, e: ft.DragUpdateEvent) -> None:
        if self.content.margin.top < (25 + 8) and e.delta_y >= 0:
            self.content.margin.top += min(0.8, e.delta_y) * 5
            self.content.update()

    def _on_pan_end(self, e: ft.DragEndEvent = None) -> None:
        check_margin: bool = self.content.margin.top >= (25 + 8) if not Platform.is_desktop(self.page) else True
        if check_margin and not self.is_loading() and self._user_id is not None:
            self.set_login(self._user_id)

        self.content.margin.top = 25
        self.content.update()

    def set_loading(self, on: bool) -> None:
        self.page.views[0].disabled = on
        self.card_title.content.controls[0].update()
        self.card_title.toggle_loading_mode(on)
        self.page.update()

    def is_loading(self) -> bool:
        return self.page.views[0].disabled

    @property
    def card_height(self) -> int:
        return 320

    @property
    def _user(self) -> User:
        return User.get_user(self._user_id)