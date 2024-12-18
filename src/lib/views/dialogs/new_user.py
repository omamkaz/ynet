#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import Dialogs
from ...models.user import User
from .user import UserDialog


class NewUserDialog(UserDialog):
    def __init__(self, page: ft.Page):
        super().__init__(page, ft.Icons.PERSON_ADD_ALT_ROUNDED)
        self._change_account_type(page.client_storage.get("tab_switch") or 0)

    def on_submit(self, e: ft.ControlEvent = None):
        super().on_submit(e)

        atype = int(self.drop_down.current.value)
        if not self.valid_user(atype):
            return

        # check for exists user
        for user in User.get_users():
            if user.atype == atype and user.username == self.username.value:
                Dialogs.error("هاذا المستخدم موجود مسبقا!", self.page)
                return

        User.add_user(
            atype,
            self.username.value, 
            self.password.value or (None if atype != 0 else "123456"),
            self.dname.value,
            None,
            None
        )

        self.on_submit_done()