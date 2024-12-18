#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from .constant import Platform, Refs, ThemeController
from .views.bottom_bar import BottomAppBar
from .views.cards import Cards
from .views.list_user import UserListView
from .views.tab_switch import TabSwitch


class Application:
    def on_close_window(self, e=None):
        size: tuple[int] = self.page.window.width, self.page.window.height
        self.page.client_storage.set("size", size)
        self.page.update()

    def set_current_user(self) -> None:
        cur_user_index: int = self.page.client_storage.get("cur_user") or 0
        if not Refs.users.current.controls or cur_user_index < 0:
            Refs.cards.current.toggle_card(3)
            return

        Refs.users.current.select_item(cur_user_index)

    def __call__(self, page: ft.Page) -> None:
        self.page = page

        page.padding = 0
        page.expand = True

        page.window.wait_until_ready_to_show = True
        page.horizontal_alignment = page.vertical_alignment = "center"

        page.title = "ynet"
        page.window.icon = "icon.png"
        page.theme_mode = ThemeController.get_theme_mode(page)
        page.fonts = {"linaround": "fonts/linaround_regular.otf"}

        ThemeController.set_theme_color(ThemeController.get_theme_color(page), page)

        ft.SystemOverlayStyle.enforce_system_status_bar_contrast = True
        ft.SystemOverlayStyle.enforce_system_navigation_bar_contrast = True

        if Platform.is_desktop(page):
            page.on_close = self.on_close_window

            page.window.min_width = 360
            page.window.min_height = 600

            page.window.max_width = 600
            page.window.max_height = 750

            size = (
                page.client_storage.get("size")
                if page.client_storage.contains_key("size")
                else (360, 700)
            )
            page.window.width, page.window.height = size

        page.bottom_appbar = BottomAppBar(page)
        page.floating_action_button_location = (
            ft.FloatingActionButtonLocation.CENTER_DOCKED
        )
        page.floating_action_button = ft.FloatingActionButton(
            mini=True,
            icon=ft.Icons.ADD,
            on_click=lambda e: Cards.open_new_user_dialog(page),
        )

        page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    padding=ft.padding.only(top=5),
                                    margin=0,
                                    height=250,
                                    border_radius=ft.BorderRadius(0, 0, 42, 42),
                                    bgcolor=page.theme.color_scheme_seed,
                                    content=ft.Text(
                                        value = "⭭ اسحب للأسفل للتحديث", 
                                        size=11,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    alignment=ft.alignment.top_center,
                                ),
                                Cards(page, ref=Refs.cards),
                            ]
                        ),
                        TabSwitch(page),
                        ft.Stack(
                            controls=[
                                UserListView(page, ref=Refs.users),
                                ft.Container(
                                    content=ft.Image(
                                        src="empty.png",
                                        width=128 * 2,
                                        height=128 * 2
                                    ),
                                    alignment=ft.alignment.center,
                                    visible=not any(c.visible for c in Refs.users.current.controls)
                                )
                            ],
                            ref=Refs.body,
                            expand=True,
                        ),
                    ],
                ),
            )
        )

        self.set_current_user()
