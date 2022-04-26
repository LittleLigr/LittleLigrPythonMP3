import pathlib
from abc import ABCMeta
from tkinter import CENTER, NO

import pygubu
import tkinter as tk
from tkinter import ttk


class View:
    __metaclass__ = ABCMeta

    def __init__(self, path, master=None):
        self.builder = builder = pygubu.Builder()
        project_path = pathlib.Path(__file__).parent
        project_ui = project_path / path
        builder.add_resource_path(project_path)
        builder.add_from_file(project_ui)
        builder.connect_callbacks(self)

    def _apply_visual_settings(self, builder):
        pass


class AppView(View):
    def __init__(self, path, layout_name, master=None):
        super().__init__(path, master)
        self.main_window = self.builder.get_object(layout_name)
        self.center_frame = self.builder.get_object("centerFrame")
        self._apply_visual_settings(self.builder)

        self.album_label = self.builder.get_object("albumLabel")
        self.artist_label = self.builder.get_object("artistLabel")
        self.song_artwork = self.builder.get_object("songArtwork")
        self.menu = self.builder.get_object("menuTree")
        self.play_button = self.builder.get_object("playButton")

        self._generate_tree_style('app.Treeview')

        self._generate_columns(self.menu)
        self.menu.configure(style='app.Treeview')

        self.menu_icons = []
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-musical-notes-30_white.png"))
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-favorite-30_white.png"))
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-music-album-30_white.png"))
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-settings-30.png"))

        self.menu.insert("", 'end', image=self.menu_icons[0], text="some text", values=("", "Music"))
        self.menu.insert("", 'end', image=self.menu_icons[1], values=("", "Favourites"))
        self.menu.insert("", 'end', image=self.menu_icons[2], values=("", "Albums"))
        self.menu.insert("", 'end', image=self.menu_icons[3], values=("", "Settings"))

    def run(self):
        self.main_window.mainloop()

    def _generate_tree_style(self, name):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(name, background="#dddbec",
                        fieldbackground="#dddbec", foreground="black", borderwidth=0)
        style.map(name, background=[('selected', '#f8f8fb')], foreground=[('selected', '#000000')])
        style.configure(name, rowheight=50)
        style.configure(name, font=('Yu Gothic UI Semilight', 14))

    def _generate_columns(self, tree):
        tree['show'] = "tree"
        tree['columns'] = ('#1', '#2')
        tree.column('#0', anchor='w', width=40, stretch=NO)
        tree.column('#1', anchor='w', width=10, stretch=NO)
        tree.column('#2', anchor='w', width=40)

        tree.heading("#0", text="1")
        tree.heading("#1", text="2")
        tree.heading("#1", text="3")

    def fill_music_bar(self, artist, album, artwork):
        self.album_label.configure(text=album)
        self.artist_label.configure(text=artist)
        self.song_artwork.configure(image=artwork)
        pass


class SongsView(View):
    def __init__(self, path, layout_name, master=None):
        super().__init__(path, master)
        self.ui = self.builder.get_object(layout_name, master)
        self._apply_visual_settings(self.builder)

        self.addMusicButton = self.builder.get_object('addMusicButton')

        self._generate_tree_style('songs.Treeview')
        self.songs_tree = self.builder.get_object('songsList')
        self.songs_tree.configure(style='songs.Treeview')
        self.songs_tree['show'] = "tree"

        self.songs_tree['columns'] = ('#1', '#2', '#3')
        self.songs_tree.column('#0', anchor=CENTER, width=40, stretch=NO)
        self.songs_tree.column('#1', width=40, stretch=NO)
        self.songs_tree.column('#2', anchor='w', width=40)
        self.songs_tree.column('#3', anchor=CENTER, width=80, stretch=NO)
        self.songs_tree.heading("#0", text="")
        self.songs_tree.heading("#1", text="")
        self.songs_tree.heading("#2", text="")

    def _generate_tree_style(self, name):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(name, background="#e8e9f2",
                        fieldbackground="#e8e9f2", foreground="black", borderwidth=0)
        style.map(name, background=[('selected', '#ece4fa')], foreground=[('selected', '#000000')])
        style.configure(name, rowheight=56)
        style.configure(name, font=('Yu Gothic UI Semilight', 14))

    def insert(self, image, text, fields):
        if image is None:
            self.songs_tree.insert("", 'end', values=fields, text = text)
        else:
            self.songs_tree.insert("", 'end', image=image, text=text, values=fields)

class SettingsView(View):
    def __init__(self, path, layout_name, master=None):
        super().__init__(path, master)
        self.ui = self.builder.get_object(layout_name, master)
