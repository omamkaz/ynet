#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
import requests

from ...constant import Dialogs
from ...models.user import User
from ...scrapper.adsl import ADSL


class CreditCardDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page, user_id: int):
        super().__init__(ft.Control)

        self.page = page

        self.isp = ADSL()
        self.isp.set_cookies(User.get_user(user_id).cookies)

        self.enable_drag = True
        self.use_safe_area = True
        self.show_drag_handle = True
        self.is_scroll_controlled = True

        self.msg_label = ft.Ref[ft.Text]()

        self.content = ft.SafeArea(
            minimum_padding=8,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.ListView(
                        expand=True,
                        spacing=12,
                        padding=8,
                        controls=[
                            ft.TextField(
                                max_length=16,
                                label=f"الكرت رقم {i + 1}"
                                + (" (اختياري) " if i > 0 else " (مطلوب) "),
                                keyboard_type=ft.KeyboardType.NUMBER,
                                input_filter=ft.NumbersOnlyInputFilter(),
                                on_focus=self.on_credit_field_focus,
                            )
                            for i in range(15)
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                text="الغاء", color=ft.Colors.RED, on_click=self.close
                            ),
                            ft.ElevatedButton(text="تجديد", on_click=self.on_submit),
                            # ft.IconButton(
                            #     icon=ft.Icons.ADD,
                            #     on_click=self.on_add_card_number,
                            # ),
                        ],
                    ),
                    ft.Text(ref=self.msg_label, color=ft.Colors.RED, size=14),
                ],
            ),
        )

        # self.add_card_number()

    # def on_add_card_number(self, e):
    #     self.add_card_number()
    #     self.update()

    # def on_delete_card_number(self, e):
    #     controls = self.content.content.controls[0].controls
    #     if e.control.data >= 1:
    #         controls.pop(e.control.data)

    #     self.content.content.controls[1].controls[-1].disabled = len(controls) >= 14
    #     self.update()

    # def add_card_number(self) -> None:
    #     controls = self.content.content.controls[0].controls

    #     i = len(controls)
    #     if i < 15:
    #         controls.append(
    #             ft.Row(
    #                 expand=True,
    #                 controls=[
    #                     ft.TextField(
    #                         max_length=16,
    #                         label=f"ادخل رقم الكرت"
    #                         + (" (اختياري) " if i >= 1 else " (مطلوب) "),
    #                         keyboard_type=ft.KeyboardType.NUMBER,
    #                         input_filter=ft.NumbersOnlyInputFilter(),
    #                         on_focus=self.on_credit_field_focus,
    #                         expand=True,
    #                     ),
    #                     ft.IconButton(
    #                         ft.Icons.DELETE,
    #                         on_click=self.on_delete_card_number,
    #                         data=i,
    #                         visible=i >= 1,
    #                     ),
    #                 ],
    #             )
    #         )

    #     self.content.content.controls[1].controls[-1].disabled = i >= 14

    def on_credit_field_focus(self, e: ft.ControlEvent = None):
        fields = self.content.content.controls[0].controls
        fields[0].error_text = (
            "الكرت الاول مطلوب"
            if e.control != fields[0] and not fields[0].value
            else None
        )
        self.update()

    def close(self, e: ft.ControlEvent = None):
        self.page.close(self)

    def on_submit(self, e: ft.ControlEvent = None):
        self.content.disabled = True
        self.update()

        # reset err msg if exists
        self.msg_label.current.value = None
        self.msg_label.current.update()

        fields = self.content.content.controls[0].controls
        if not fields[0].value:
            return

        try:
            _, err = self.isp.fetch_credit([card.value for card in fields])
            if err is not None:
                self.msg_label.current.value = err
                self.msg_label.current.update()
        except requests.exceptions.Timeout:
            Dialogs.connection_timeout(self.page)
        except requests.exceptions.ConnectionError:
            Dialogs.no_internet_connection(self.page)
        except Exception as err:
            Dialogs.error(err, self.page)

        self.content.disabled = False
        self.update()
