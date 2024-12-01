#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft
from lib.models.base import DBEngine
from lib.constant import APP_VERSION
from lib.app import Application


__version__ = APP_VERSION


if __name__ == "__main__":
    DBEngine.init_db()
    DBEngine.init_tables()

    ft.app(
        target=Application(),
        name="ynet"
    )