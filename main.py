#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from src.lib.models.base import DBEngine
from src.lib.constant import APP_VERSION
from src.lib.app import Application


__version__ = APP_VERSION


if __name__ == "__main__":
    DBEngine.init_db()
    DBEngine.init_tables()

    ft.app(
        target=Application(),
        name="ynet"
    )