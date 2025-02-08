#!/usr/bin/python3
# -*- coding: utf-8 -*-

import flet as ft

from lib.app import Application
from lib.constant import APP_VERSION
from lib.models.base import DBEngine

__version__ = APP_VERSION

# Avoid SSL Warnings
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


if __name__ == "__main__":
    DBEngine.init_db()
    DBEngine.init_tables()

    ft.app(target=Application(), name="ynet")
