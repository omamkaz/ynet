#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import UserData


class CardCredit(ft.Container):
    def __init__(self):
        super().__init__()

        self.padding = 0
        self.margin = 0
        self.expand = True
        self.content = ft.Column(
            spacing=6,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="الرصيد المتاح",
                    color=ft.Colors.WHITE,
                    size=14,
                    rtl=True
                ),
                ft.Text(
                    size = 18,
                    color = ft.Colors.WHITE,
                    font_family="Monospace",
                    weight=ft.FontWeight.W_700,
                    text_align="center",
                    spans=[
                        ft.TextSpan(
                            style = ft.TextStyle(
                                color = ft.Colors.GREEN,
                                size = 12
                            ),
                            visible=False
                        )
                    ]
                )
            ]
        )

    def hide_credit_state(self):
        span = self.content.controls[-1].spans[0]
        span.visible = False
        span.update()

    def show_credit_state(self):
        span = self.content.controls[-1].spans[0]
        span.visible = True
        span.update()

    def _credit_state(self, value: str, color: str, prefix: str) -> None:
        span = self.content.controls[-1].spans[0]
        span.style.color = color
        span.text = (" " * 1) + f"{prefix}{value}"
        span.visible = True
        span.update()

    def increment(self, value: str) -> None:
        self._credit_state(value, "green", "+")

    def decrement(self, value: str) -> None:
        self._credit_state(value, "red", "-")

    def set_credit(self, value: str):
        credit = self.content.controls[-1]
        credit.value = value
        credit.update()

    def set_credit_state(self, data: dict[str, str], old_data: dict[str, str]) -> None:
        def get_value(var):
            return float(var.get("valid_credit").split()[0].strip())

        if not old_data:
            self.hide_credit_state()
            return

        old_value = get_value(old_data)
        new_value = get_value(data)

        self.show_credit_state()

        if new_value < old_value:
            self.decrement(UserData.custom_credit(old_value - new_value))
        elif new_value > old_value:
            self.increment(UserData.custom_credit(new_value - old_value))
        else:
            self.hide_credit_state()

        self.update()
