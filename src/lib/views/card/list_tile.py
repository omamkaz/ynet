#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ...constant import LottieFiles, Platform


class CardTitle(ft.ListTile):
    def __init__(self, page: ft.Page, atype: int | str = 0):
        super().__init__()

        self.page = page
        self.content_padding = ft.padding.only(right=10)

        self.title = ft.Text(
            size=14.5,
            color=ft.Colors.WHITE,
            text_align="right"
        )

        self.subtitle = ft.Text(
            text_align="right",
            color=ft.Colors.WHITE70,
            size=14
        )

        self.trailing = ft.Stack(
            alignment=ft.alignment.bottom_right,
            controls=[
                ft.Image(
                    src=f"/atype/{atype}.png",
                    width=42,
                    height=42,
                    badge=ft.Badge(
                        small_size=13,
                        bgcolor=ft.Colors.GREEN
                    )
                )
            ]
        )

        self.leading = ft.Stack(
            controls=[
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    visible=Platform.is_desktop(self.page)

                ),
                ft.Lottie(
                    # src=LottieFiles.down_arrow,
                    src_base64=LottieFiles.down_arrow,
                    visible=not Platform.is_desktop(self.page)
                )
            ]
        )

    def toggle_loading_mode(self, on: bool) -> None:
        self.leading.controls[1].visible = True
        # self.leading.controls[1].src = LottieFiles.loading_carga if on else LottieFiles.down_arrow
        self.leading.controls[1].src_base64 = LottieFiles.loading_carga if on else LottieFiles.down_arrow

        if Platform.is_desktop(self.page):
            self.leading.controls[0].visible = not on
            self.leading.controls[1].visible = on
        
        self.update()

    def set_active(self, on: bool = True) -> None:
        self.trailing.controls[-1].bgcolor = "green" if on else "red"
        self.update()

    def set_logo(self, atype: int | str) -> None:
        self.trailing.controls[0].src = f"/atype/{atype}.png"
        self.update()

    def set_title(self, title: str) -> None:
        self.title.value = title
        self.update()

    def set_subtitle(self, subtitle: str) -> None:
        self.subtitle.value = subtitle
        self.update()
