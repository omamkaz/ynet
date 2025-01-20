#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import Refs
from ...models.user import User
from ..dialogs import EditUserDialog
from ..dialogs.credit_card import CreditCardDialog


class UserListTile(ft.ListTile):
    def __init__(self, page: ft.Page, index: int, user, **kwargs):
        super().__init__(**kwargs)

        self.page = page

        self._index = index
        self._user = user

        self.on_click = self._on_click

        self.title = ft.Text(value=user.dname or f"حساب رقم {index}", rtl=True)
        self.subtitle = ft.Text(value=user.username, rtl=True)

        self.trailing = ft.Stack(
            alignment=ft.alignment.bottom_right,
            controls=[
                ft.Image(src=f"atype/{user.atype}.png", width=38, height=38),
                ft.Icon(
                    name=ft.Icons.VERIFIED,
                    color=ft.Colors.BLUE,
                    size=16,
                    visible=user.data is not None,
                ),
            ],
        )

        self.leading = ft.PopupMenuButton(
            tooltip="خيارات اخرى",
            items=[
                ft.PopupMenuItem(
                    text="تجديد",
                    icon=ft.Icons.CREDIT_CARD,
                    on_click=self.on_credit,
                    disabled=user.atype != 0,
                ),
                ft.PopupMenuItem(
                    text="تعديل", icon=ft.Icons.EDIT, on_click=self.on_edit
                ),
                ft.PopupMenuItem(
                    text="حذف", icon=ft.Icons.DELETE, on_click=self.on_delete
                ),
            ],
        )

        self.selected_tile_color = ft.Colors.with_opacity(
            0.09, self.page.theme.color_scheme_seed
        )

    def _on_click(self, e: ft.ControlEvent = None) -> None:
        Refs.users.current.select_item(self)

    def on_delete(self, e: ft.ControlEvent = None) -> None:
        def on_ok():
            self.page.close(alert)
            self.page.client_storage.set("cur_user", 0)

            User.delete_user(self._user.id)
            Refs.users.current.update_list()

            if Refs.users.current.controls:
                Refs.users.current.select_item(0)
            else:
                Refs.cards.current.toggle_card(3)

        alert = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                value="هل أنت متأكد من انك تريد حذف ",
                spans=[
                    ft.TextSpan(
                        text=self.title.value,
                        style=ft.TextStyle(
                            color=ft.Colors.RED, weight=ft.FontWeight.BOLD
                        ),
                    )
                ],
                rtl=True,
            ),
            actions=[
                ft.ElevatedButton(text="نعم", on_click=lambda e: on_ok()),
                ft.ElevatedButton(
                    text="لا", autofocus=True, on_click=lambda e: self.page.close(alert)
                ),
            ],
        )
        self.page.open(alert)

    def set_verified(self, on: bool) -> None:
        self.trailing.controls[-1].visible = on
        self.trailing.update()

    def on_edit(self, e: ft.ControlEvent = None):
        user_view_edit = EditUserDialog(self.page, self._user.id)
        self.page.open(user_view_edit)

    def on_credit(self, e: ft.ControlEvent = None) -> None:
        credit_card_dialog = CreditCardDialog(self.page, self._user.id)
        credit_card_dialog.open_dialog()
