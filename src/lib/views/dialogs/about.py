#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import ABOUT_LINK_ICONS, APP_VERSION


class LinkIcon(ft.IconButton):
    def __init__(self, icon: str, color: str, link: str, page: ft.Page):
        super().__init__()

        self.page = page
        self.link = link
        self.tooltip = icon.title()
        self.on_click = self.on_open_url

        self.content = ft.Image(
            src=f"/logo/{icon}.svg", color=color, width=18, height=18
        )

    def on_open_url(self, e: ft.ControlEvent) -> None:
        if self.page.can_launch_url(self.link):
            self.page.launch_url(self.link)


class AboutDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page):
        super().__init__(ft.Control)

        self.page = page

        self.enable_drag = True
        self.show_drag_handle = True

        self.content = ft.SafeArea(
            minimum_padding=ft.padding.only(left=5, right=5),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment="center",
                controls=[
                    ft.Text(value="عن المطور", weight=ft.FontWeight.BOLD),
                    ft.Container(
                        width=64,
                        height=64,
                        shape=ft.BoxShape("circle"),
                        image=ft.DecorationImage(src="/developer.jpg", fit="cover"),
                    ),
                    ft.Text(value="Osama Mohammed AL-Zabidi", size=14),
                    ft.Text(
                        "Software Developer | Python Programming | GUI & Web Apps",
                        weight="w400",
                        text_align="center",
                        size=10,
                    ),
                    ft.Container(
                        margin=ft.margin.only(10, 20, 10),
                        content=ft.Column(
                            spacing=16,
                            controls=[
                                ft.TextField(
                                    value="@omamkaz",
                                    read_only=True,
                                    label="Username",
                                    height=50,
                                    border_radius=5,
                                    cursor_height=16,
                                    content_padding=10,
                                    border_width=1.5,
                                    text_size=14,
                                    on_focus=lambda e: self.page.set_clipboard(
                                        e.control.value
                                    ),
                                ),
                                ft.Row(
                                    spacing=0,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        LinkIcon(icon, color, link, page)
                                        for icon, color, link in ABOUT_LINK_ICONS
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        alignment=ft.alignment.center,
                        margin=ft.margin.only(right=10, bottom=10, left=10),
                        content=ft.Text(
                            value=APP_VERSION,
                            weight=ft.FontWeight.BOLD,
                            font_family="Monospace",
                            text_align="center",
                            size=13,
                        ),
                    ),
                ],
            ),
        )
