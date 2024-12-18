#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import Refs
from ...models.user import User
from .list_tile import UserListTile


class UserListView(ft.Column):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)

        self.page = page
        self.spacing = 6
        self.expand = True
        self.scroll = ft.ScrollMode.HIDDEN

        tab_switch = self.page.client_storage.get("tab_switch")
        self.controls = [
            self.new_item(index, user, tab_switch or 0)
            for index, user in enumerate(User.get_users(), 1)
        ]

    def new_item(self, index: int, user, tab_switch: int = 0) -> UserListTile:
        return UserListTile(
            page=self.page,
            index=index,
            atype=user.atype,
            title=user.dname or f"حساب رقم {index}",
            subtitle=user.username,
            verified=user.data is not None,
            data=user.id,
            visible = tab_switch == user.atype
        )

    def update_list(self):
        self.controls.clear()

        tab_switch = self.page.client_storage.get("tab_switch")
        for index, user in enumerate(User.get_users(), 1):
            self.controls.append(self.new_item(index, user, tab_switch or 0))

        self.set_selected_item(self.page.client_storage.get("cur_user"))
        self.update_body()
        self.update()

    def update_body(self) -> bool:
        check: bool = False
        if self.controls:
            check = any(c.visible for c in self.controls)

        Refs.body.current.controls[1].visible = not check
        Refs.body.current.update()

    def set_selected_item(self, control: UserListTile | int) -> None:
        if self.controls:
            if isinstance(control, int):
                control = self.controls[control]

            for c in self.controls:
                c.selected = (c == control)

            self.update()

    def select_item(self, control: UserListTile | int) -> None:
        if self.controls:
            if isinstance(control, int):
                control = self.controls[control]

            self.page.client_storage.set("cur_user", control._index - 1)

            Refs.users.current.set_selected_item(control)
            Refs.cards.current.get_card(control._atype).set_data(control.data)