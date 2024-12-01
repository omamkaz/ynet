#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from ..constant import Refs, ACCOUNT_TYPES


class TabSwitch(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        initial_value=0,
        **kwargs):
        super().__init__(**kwargs)

        self.page = page

        store_value: int | None = self.page.client_storage.get("tab_switch")
        self.value = store_value if store_value is not None else initial_value

        self.tabs = [
            self.get_container(index, label, index == self.value)
            for index, label in enumerate(ACCOUNT_TYPES)
        ]

        # Initialize the row with the tabs inside the main container
        self.content = ft.Row(
            controls=self.tabs,
            alignment=ft.MainAxisAlignment.CENTER, 
            scroll=ft.ScrollMode.HIDDEN,
            expand=True
        )

    def get_container(self, index: int, text: str, active: bool):
        """Create an individual tab container based on active status."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        value=text,
                        size=15,
                    ),
                    ft.Image(
                        src=f"/atype/{index}.png",
                        width=32,
                        height=32
                    )
                ]
            ),
            bgcolor=self.page.theme.color_scheme_seed if active else None,
            border_radius=8,
            alignment=ft.alignment.center,
            padding=5,
            animate=ft.animation.Animation(
                duration=300, 
                curve=ft.AnimationCurve.DECELERATE
            ),
            on_click=self.toggle_switch
        )

    def toggle_switch(self, e):
        """Switch to the tab that was clicked and update its appearance."""
        new_active_index = self.content.controls.index(e.control)
        if new_active_index != self.value:
            self.update_tab(self.tabs[self.value], False)
            self.update_tab(self.tabs[new_active_index], True)
            self.value = new_active_index

            self.page.client_storage.set("tab_switch", new_active_index)
            self.page.update()

            # Code to switch list account types
            Refs.users.current.update_list()

    def update_tab(self, tab, active):
        """Update the visual state of a tab."""
        tab.bgcolor = (
            self.page.theme.color_scheme_seed
            if active
            else None
        )
        tab.update()
