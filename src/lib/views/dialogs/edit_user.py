#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import Dialogs
from ...models.user import User
from .user import UserDialog


class EditUserDialog(UserDialog):
    def __init__(self, page: ft.Page, user_id: int):
        super().__init__(page, ft.Icons.MODE_EDIT)

        self.user = User.get_user(user_id)
        self._change_account_type(self.user.atype)

        self.dname.value = self.user.dname
        self.username.value = self.user.username
        if self.user.atype == 0:
            self.password.value = self.user.password

    def on_submit(self, e: ft.ControlEvent = None):
        super().on_submit(e)

        atype: int = int(self.drop_down.current.value)
        if not self.valid_user(atype):
            return

        # check for exists user
        for user in User.get_users():
            if (
                user.id != self.user.id
                and user.atype == atype
                and user.username == self.username.value
            ):
                Dialogs.error("هاذا المستخدم موجود مسبقا!", self.page)
                return

        User.edit_user(
            self.user.id,
            atype,
            self.username.value,
            self.password.value,
            self.dname.value,
        )

        self.on_submit_done()
