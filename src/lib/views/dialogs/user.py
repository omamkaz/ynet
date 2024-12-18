#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from ...constant import ACCOUNT_TYPES, Platform, Refs


class TextField(ft.TextField):
    def __init__(self,
                 page: ft.Page,
                 label: str, 
                 regex: str = "^[a-zA-Z0-9]*$",
                 required: bool = False,
                 suffix_visible: bool = False,
                 **kwargs):
        super().__init__(label=label, **kwargs)

        self.page = page

        self.max_length = 32
        self.text_align = "center"
        self.input_filter = ft.InputFilter(regex)

        self.suffix = ft.IconButton(
            icon=ft.Icons.NUMBERS,
            on_click=self.change_input_type,
            visible=suffix_visible and not Platform.is_desktop(page)
        )

        if required:
            self.on_change = self.on_text_changed

        self.counter_text = f"{len(self.value)}/{self.max_length}"

    def on_text_changed(self, e: ft.ControlEvent = None):
        self.error_text = "هاذا الحقل مطلوب" if not self.value.strip() else None
        self.counter_text = f"{len(self.value)}/{self.max_length}"
        self.update()

    def change_input_type(self, e: ft.ControlEvent = None):
        self.keyboard_type = None if self.keyboard_type is not None else ft.KeyboardType.NUMBER
        self.suffix.selected = self.keyboard_type is not None
        self.update()

    def toggle_suffix(self, on: bool) -> None:
        self.suffix.visible = on and not Platform.is_desktop(self.page)


class DropdownOption(ft.dropdown.Option):
    def __init__(self, index: int, atype: str, **kwargs):
        super().__init__(index, **kwargs)
    
        self.content = ft.Row(
            controls=[
                ft.Image(
                    src=f"/atype/{index}.png",
                    width=32,
                    height=32
                ),
                ft.Text(
                    value=atype,
                    rtl=True
                )
            ]
        )


class UserDialog(ft.BottomSheet):
    def __init__(self, page: ft.Page, view_type_icon: str):
        super().__init__(ft.Control)

        self.page = page

        self.enable_drag = True
        self.use_safe_area = True
        self.show_drag_handle = True
        self.is_scroll_controlled = True

        self.logo = ft.Ref[ft.Container]()
        self.title = ft.Ref[ft.Text]()
        self.drop_down = ft.Ref[ft.Dropdown]()

        self.dname = TextField(
            page=self.page, 
            label="الاسم المستعار", 
            regex=""
        )

        self.username = TextField(
            page=self.page,
            label="أسم المستخدم",
            required=True,
            on_submit=self.on_submit,
            suffix_visible=True
        )

        self.password = TextField(
            page=self.page,
            value = "123456",
            label="كلمة السر",
            password=True,
            can_reveal_password=True,
            on_submit=self.on_submit,
            suffix_visible=True
        )

        self.content = ft.SafeArea(
            minimum_padding=ft.padding.only(left=15, right=15),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Image(
                        ref=self.logo,
                        width=64,
                        height=64,
                        src="/atype/0.png"
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                ref=self.title,
                                value=ACCOUNT_TYPES[0],
                                weight=ft.FontWeight.W_500,
                                size=16,
                                rtl=True
                            ),
                            ft.Icon(name=view_type_icon)
                        ]
                    ),
                    ft.Divider(10, color=ft.Colors.TRANSPARENT),
                    ft.Dropdown(
                        ref=self.drop_down,
                        label="نوع الحساب",
                        value=0,
                        autofocus=True,
                        on_change=lambda e: self.change_account_type(int(self.drop_down.current.value)),
                        options=[
                            DropdownOption(index, atype)
                            for index, atype in enumerate(ACCOUNT_TYPES)
                        ]
                    ),
                    ft.Divider(10, color=ft.Colors.TRANSPARENT),
                    self.dname,
                    self.username,
                    self.password,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.ElevatedButton(
                                text = "الغاء", 
                                color = ft.Colors.RED,
                                on_click=lambda e: self.close()
                            ),
                            ft.ElevatedButton(
                                text = "حفظ",
                                on_click=self.on_submit
                            )
                        ]
                    )
                ]
            )
        )

    def close(self):
        self.page.close(self)

    def on_submit_done(self):
        Refs.users.current.update_list()
        Refs.users.current.set_selected_item(Refs.users.current.controls[-1])
        Refs.users.current.select_item(-1)
        self.close()

    def _change_account_type(self, atype: int) -> None:
        self.drop_down.current.value = atype

        self.password.visible = (atype == 0)

        self.title.current.value = ACCOUNT_TYPES[atype]
        self.logo.current.src = f"/atype/{atype}.png"

        self.username.value = "" if atype != 1 else "10"

        self.username.max_length = (9, 8)[atype - 1] if atype != 0 else 32
        self.username.keyboard_type = ft.KeyboardType.NUMBER if atype != 0 else None
        self.username.input_filter = ft.InputFilter(
            regex_string=(r"^[a-zA-Z0-9]*$", r"^10[0-9]*$", r"^[0-9]*$")[atype]
        )

        self.username.toggle_suffix(atype == 0)
        self.password.toggle_suffix(atype == 0)

    def change_account_type(self, atype: int) -> None:
        self._change_account_type(atype)
        self.username.update()
        self.password.update()
        self.update()

    def valid_user(self, atype: int = 0) -> bool | None:
        return not (not self.username.value.strip() 
                    or self.username.error_text
                    or atype != 0 and (len(self.username.value) < self.username.max_length))

    def on_submit(self, e: ft.ControlEvent):
        self.username.on_text_changed()