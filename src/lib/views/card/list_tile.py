#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ...constant import LottieFiles, Platform, ThemeController


class CardTitle(ft.ListTile):
    def __init__(self, 
                 page: ft.Page, 
                 atype: int | str = 0, 
                 **kwargs):
        super().__init__(**kwargs)

        self.page = page

        self.bgcolor = ThemeController.get_color(self.page.theme.color_scheme_seed, 800)
        self.content_padding = ft.padding.only(right=10, left=(10 if Platform.is_desktop(page) else 0))

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

        self.trailing = ft.Image(
            src=f"/atype/{atype}.png",
            width=48,
            height=48,
            badge=ft.Badge(
                small_size=13,
                bgcolor=ft.Colors.GREEN,
                alignment=ft.alignment.top_right
            )
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
        self.trailing.badge.bgcolor = "green" if on else "red"
        self.update()

    def set_logo(self, atype: int | str) -> None:
        self.trailing.src = f"/atype/{atype}.png"
        self.update()

    def set_title(self, title: str) -> None:
        self.title.value = title
        self.update()

    def set_subtitle(self, subtitle: str) -> None:
        self.subtitle.value = subtitle
        self.update()
