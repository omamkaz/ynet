#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests

from ...constant import Dialogs, Refs
from ...models.user import User
from .credit import CardCredit
from .item import CardItem
from .title import CardTitle


class Card(ft.GestureDetector):
    _user_id: int = None
    _isp = None

    def __init__(self, page: ft.Page, atype: int | str, **kwargs):
        super().__init__(**kwargs)

        self.page = page

        self.card_title: CardTitle = CardTitle(page, atype)
        self.card_credit: CardCredit = CardCredit()
        self.card_items = ft.Ref[ft.Column]()

        self.on_pan_end = lambda _: self._on_pan_end()
        self.on_pan_update = self._on_pan_update

        self.content = ft.Container(
            expand=True,
            padding=0,
            border_radius=16,
            height=self.card_height,
            alignment=ft.alignment.center,
            margin=ft.margin.only(left=14, right=14, top=25),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_IN_OUT),
            shadow=ft.BoxShadow(
                spread_radius=-10,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.07, ft.Colors.BLACK),
                offset=ft.Offset(0, 8),
            ),
            content=ft.Column(
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.card_title,
                    self.card_credit,
                    ft.Column(
                        ref=self.card_items,
                        spacing=0,
                        expand=True,
                        scroll=ft.ScrollMode.HIDDEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN, visible=atype != 2),
                ],
            ),
        )

        self.card_title.content.controls[0].controls[0].on_click = (
            lambda _: self._on_pan_end(True)
        )

    def set_card_items(self, data: dict[str, str]) -> None:
        self.card_items.current.controls.clear()

        _data = data.copy()
        _data.pop("warn", None)
        _len = len(_data)

        if self._user.last_update is not None:
            _data["تاريخ اخر تحديث"] = self._user.last_update.strftime("%A %d/%m/%Y %r")

        self.card_items.current.controls.extend(
            CardItem(label, value, end=index == _len)
            for index, (label, value) in enumerate(_data.items())
        )

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
        cookies: dict[str, str] = None,
    ) -> None:

        Refs.cards.current.toggle_card(atype)

        User.edit_data_and_cookies(self._user_id, data, cookies)
        self.set_card_data(old_data)

        for c in Refs.users.current.controls:
            c.selected = self._user_id == c._user.id
            c.set_verified(c._user.data is not None)
        Refs.users.current.update()

    def _on_pan_update(self, e: ft.DragUpdateEvent) -> None:
        if self.content.margin.top < (25 + 8) and e.delta_y >= 0:
            self.content.margin.top += min(0.8, e.delta_y) * 5
            self.content.update()

    def _on_pan_end(self, is_desktop: bool = False) -> None:
        check_margin: bool = self.content.margin.top >= (25 + 8) or is_desktop
        if check_margin and not self.is_loading() and self._user_id is not None:
            self.set_login(self._user_id)

        self.content.margin.top = 25
        self.content.update()

    def set_loading(self, on: bool) -> None:
        self.page.views[0].disabled = on
        self.card_title.toggle_loading_mode(on)
        self.page.update()

    def is_loading(self) -> bool:
        return self.page.views[0].disabled

    @property
    def card_height(self) -> int:
        return 280

    @property
    def _user(self) -> User:
        return User.get_user(self._user_id)
