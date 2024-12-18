#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import LottieFiles, Platform


class CardTitle(ft.Container):
    def __init__(self, 
                 page: ft.Page, 
                 atype: int | str = 0, 
                 **kwargs):
        super().__init__(**kwargs)

        self.page = page
        self.padding = 10

        self.loading_mode = ft.Ref[ft.Lottie]()
        
        self.content = ft.Row(
            controls=[
                ft.Stack(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            visible=Platform.is_desktop(self.page)
                        ),
                        ft.Lottie(
                            ref=self.loading_mode,
                            src_base64=LottieFiles.down_arrow,
                            visible=not Platform.is_desktop(self.page),
                            fit=ft.ImageFit.COVER
                        )
                    ],
                    width=48,
                    height=48,
                    expand=False
                ),

                ft.Column(
                    controls=[
                        ft.Text(
                            size=14.5,
                            color=ft.Colors.WHITE,
                            text_align="right"
                        ),
                        ft.Text(
                            text_align="right",
                            color=ft.Colors.WHITE70,
                            size=14
                        )
                    ],
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.END,
                    spacing=0
                ),

                ft.Image(
                    src=f"/atype/{atype}.png",
                    width=48,
                    height=48,
                    badge=ft.Badge(
                        small_size=15,
                        bgcolor=ft.Colors.GREEN,
                        alignment=ft.alignment.top_right,
                        
                    ),
                    expand=False
                )
            ],
            expand=True
        )

    def toggle_loading_mode(self, on: bool) -> None:
        self.loading_mode.current.visible = True
        self.loading_mode.current.src_base64 = LottieFiles.loading_carga if on else LottieFiles.down_arrow

        if Platform.is_desktop(self.page):
            self.content.controls[0].controls[0].visible = not on
            self.loading_mode.current.visible = on

        self.update()

    def set_active(self, on: bool = True) -> None:
        self.content.controls[-1].badge.bgcolor = "green" if on else "red"
        self.update()

    def set_logo(self, atype: int | str) -> None:
        self.content.controls[-1].src = f"/atype/{atype}.png"
        self.update()

    def set_title(self, title: str) -> None:
        self.content.controls[1].controls[0].value = title
        self.update()

    def set_subtitle(self, subtitle: str) -> None:
        self.content.controls[1].controls[1].value = subtitle
        self.update()
