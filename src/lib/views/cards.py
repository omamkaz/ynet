#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import flet_lottie as fl

from ..constant import LottieFiles, Refs
from .card import ADSLCard, Card, LTECard, PhoneCard
from .dialogs import NewUserDialog


class Cards(ft.Stack):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)

        self.page = page
        self.controls = [
            ADSLCard(page, visible=False),
            LTECard(page, visible=False),
            PhoneCard(page, visible=False),
            ft.Container(
                content=fl.Lottie(
                    fit=ft.ImageFit.COVER, src_base64=LottieFiles.online_health_report
                ),
                alignment=ft.alignment.center,
                on_click=lambda _: self.open_new_user_dialog(self.page),
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        fl.Lottie(
                            fit=ft.ImageFit.COVER, src_base64=LottieFiles.pin_required
                        ),
                        ft.Text(value="قم بالضغط هنا لاكمال التسجيل"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                on_click=self.on_verify_click,
            ),
        ]

    def toggle_card(self, atype: int | str = 3) -> Card:
        atype = int(atype)

        top_card = self.page.controls[0].content.controls[0].controls[0]
        top_card.content.visible = 0 <= atype <= 2
        top_card.height = 250 if atype != 2 else 170
        top_card.update()

        for i, c in enumerate(self.controls):
            c.visible = i == atype

        self.update()
        return self.controls[atype]

    def get_card(self, atype: int | str) -> Card:
        return self.controls[int(atype)]

    @classmethod
    def open_new_user_dialog(cls, page: ft.Page) -> None:
        user_view_new = NewUserDialog(page)
        page.open(user_view_new)

    def on_verify_click(self, e: ft.ControlEvent) -> None:
        cur_user_index: int = self.page.client_storage.get("cur_user") or 0
        control: int = Refs.users.current.controls[cur_user_index]
        self.get_card(control._user.atype).set_login(control._user.id)
