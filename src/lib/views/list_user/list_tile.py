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

        self._warn = None
        if user.data is not None:
            self._warn = user.data.get("warn", None)

        self.on_click = self.on_item_click

        self.title = ft.Text(
            value=user.dname or f"حساب رقم {index}", rtl=True, expand=True
        )
        self.subtitle = ft.Text(value=user.username, rtl=True, expand=True)

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

        self.leading = ft.Row(
            controls=[
                ft.PopupMenuButton(
                    tooltip="خيارات اخرى",
                    items=[
                        ft.PopupMenuItem(
                            text="تجديد",
                            icon=ft.Icons.CREDIT_CARD,
                            on_click=self.on_credit,
                        ),
                        ft.PopupMenuItem(
                            text="تعديل", icon=ft.Icons.EDIT, on_click=self.on_edit
                        ),
                        ft.PopupMenuItem(
                            text="حذف", icon=ft.Icons.DELETE, on_click=self.on_delete
                        ),
                    ],
                ),
                ft.IconButton(
                    ft.Icons.WARNING,
                    on_click=self.show_warn,
                    visible=self._warn is not None,
                    tooltip="تنبية",
                ),
            ],
            width=128,
            height=128,
            expand=False,
            spacing=0,
        )

        if user.atype != 0:
            self.leading.controls[0].items.pop(0)

    def on_item_click(self, e: ft.ControlEvent = None) -> None:
        Refs.users.current.select_item(self._index)

    def on_delete(self, e: ft.ControlEvent = None) -> None:
        def on_ok():
            User.delete_user(self._user.id)

            self.page.client_storage.set("cur_user", 0)
            self.page.close(alert)

            Refs.users.current.update_list(0)
            if not Refs.users.current.controls:
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
                ft.ElevatedButton(text="نعم", on_click=lambda _: on_ok()),
                ft.ElevatedButton(
                    text="لا", autofocus=True, on_click=lambda _: self.page.close(alert)
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
        self.page.open(credit_card_dialog)

    def show_warn(self, e: ft.ControlEvent = None) -> None:
        self.page.open(
            ft.AlertDialog(
                title=ft.Text("تنبية", text_align="center"),
                icon=ft.Icon(ft.Icons.WARNING),
                content=ft.Text(self._warn, rtl=True),
            )
        )
