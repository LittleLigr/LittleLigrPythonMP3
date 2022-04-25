from abc import ABCMeta
from tinydb import TinyDB, Query
import tkinter as tk

db = TinyDB("resources/data/data.json")


class Model:
    __metaclass__ = ABCMeta

    def __init__(self, view):
        self.view = view


class AppModel(Model):

    def __init__(self, app_view):
        super().__init__(app_view)


class SongsModel(Model):

    def __init__(self, songs_view):
        super().__init__(songs_view)
        self.img = tk.PhotoImage(file="test.png")
        self.view.songs_tree.insert("", 'end', image=self.img, text="some text", values=("1", "2", "3"))


class SettingsModel(Model):

    def __init__(self, settings_view):
        super().__init__(settings_view)
