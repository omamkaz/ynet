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
            for index, user in enumerate(User.get_users())
        ]

    def new_item(self, index: int, user, tab_switch: int = 0) -> UserListTile:
        return UserListTile(self.page, index, user, visible=tab_switch == user.atype)

    def update_list(self, selected_item: int = None) -> None:
        self.controls.clear()

        tab_switch = self.page.client_storage.get("tab_switch")
        for index, user in enumerate(User.get_users()):
            self.controls.append(self.new_item(index, user, tab_switch or 0))

        selected_item = (
            selected_item
            if selected_item is not None
            else self.page.client_storage.get("cur_user")
        )

        self.select_item(selected_item)
        self.update_body()
        self.update()

    def update_body(self) -> bool:
        check: bool = any(c.visible for c in self.controls) if self.controls else False
        Refs.body.current.controls[1].visible = not check
        Refs.body.current.update()

    def select_item(self, index: int) -> None:
        if self.controls:
            prev_index = self.page.client_storage.get("cur_user") or 0
            self.update_select(prev_index, False)
            self.update_select(index, True)

            control = self.controls[index]
            Refs.cards.current.get_card(control._user.atype).set_data(control._user.id)
            self.page.client_storage.set("cur_user", index)
            self.update()

    def update_select(self, index: int, active: bool) -> None:
        control = self.controls[index]
        control.selected = active
        control.selected_tile_color = ft.Colors.with_opacity(
            0.09, self.page.theme.color_scheme_seed
        )
