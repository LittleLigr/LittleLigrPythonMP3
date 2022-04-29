import pathlib
from abc import ABCMeta
from tkinter import CENTER, NO

import pygubu
import tkinter as tk
from tkinter import ttk

import gettext

_ = None


def setup_locale(lang):
    global _
    locale = gettext.translation('locale', localedir='resources/locale', languages=[lang])
    locale.install()
    _ = locale.gettext


setup_locale('en')


class View:
    __metaclass__ = ABCMeta

    def __init__(self, path, master=None):
        self.builder = builder = pygubu.Builder()
        project_path = pathlib.Path(__file__).parent
        project_ui = project_path / path
        builder.add_resource_path(project_path)
        builder.add_from_file(project_ui)
        builder.connect_callbacks(self)

    def hide_view(self):
        self.ui.pack_forget()

    def show_view(self):
        self.ui.pack(expand=True, fill='both', side='top')

    def set_locale(self):
        pass


class AppView(View):
    pages = []

    def __init__(self, path, layout_name):
        super().__init__(path, None)
        self.main_window = self.builder.get_object(layout_name)
        self.center_frame = self.builder.get_object("centerFrame")

        self.album_label = self.builder.get_object("albumLabel")
        self.artist_label = self.builder.get_object("artistLabel")
        self.song_artwork = self.builder.get_object("songArtwork")
        self.menu = self.builder.get_object("menuTree")
        self.play_button = self.builder.get_object("playButton")
        self.next_song_button = self.builder.get_object("nextSongButton")
        self.previous_song_button = self.builder.get_object("previousSongButton")
        self.favourite_button = self.builder.get_object("favouriteButton")
        self._favourite_true_image = tk.PhotoImage(file="resources/textures/icons8-favorite-30_white.png")
        self._favourite_false_image = tk.PhotoImage(file="resources/textures/icons8-favorite-30.png")
        self._play_current_image = tk.PhotoImage(file="resources/textures/icons8-circled-play-30_colored.png")
        self._play_different_image = tk.PhotoImage(file="resources/textures/icons8-circled-play-30.png")
        self._play_paused_image = tk.PhotoImage(file="resources/textures/icons8-pause-button-30.png")
        self.delete_button = self.builder.get_object("deleteButton")
        self.music_control_frame = self.builder.get_object("musicControlFrame")
        self.sound_bar = self.builder.get_object("soundBar")
        self.volume_button = self.builder.get_object("volumeButton")
        self._silence_on_image = tk.PhotoImage(file="resources/textures/icons8-no-audio-30.png")
        self._silence_off_image = tk.PhotoImage(file="resources/textures/icons8-sound-30.png")
        self.music_little_label = self.builder.get_object("musicLittleLabel")

        self._generate_tree_style('app.Treeview')

        self._generate_columns(self.menu)
        self.menu.configure(style='app.Treeview')

        self.menu_icons = []
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-musical-notes-30_white.png"))
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-favorite-30_white.png"))
        self.menu_icons.append(tk.PhotoImage(file="resources/textures/icons8-settings-30.png"))

        self.music_little_label.config(text=_('music'))
        self.menu.insert('', 'end', image=self.menu_icons[0], values=('', _('music')))
        self.menu.insert('', 'end', image=self.menu_icons[1], values=('', _('favourites')))
        self.menu.insert('', 'end', image=self.menu_icons[2], values=('', _('settings')))

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

    def fill_music_bar(self, album, artist, image, favourite, current_playing, is_paused):
        self.album_label.configure(text=album)
        self.artist_label.configure(text=artist)
        self.song_artwork.configure(image=image)

        favourite_button_image = self._favourite_false_image
        if favourite:
            favourite_button_image = self._favourite_true_image

        if current_playing and is_paused:
            play_button_image = self._play_paused_image
        elif current_playing:
            play_button_image = self._play_current_image
        else:
            play_button_image = self._play_different_image

        self.favourite_button.configure(image=favourite_button_image)
        self.play_button.configure(image=play_button_image)
        pass

    def hide_music_bar(self):
        self.album_label.config(text='')
        self.artist_label.config(text='')
        self.song_artwork.config(text='', image='')

    def set_volume_bar_value(self, volume):
        self.sound_bar.set(volume)
        if volume == 0:
            self.volume_button.config(image=self._silence_on_image)
        else:
            self.volume_button.config(image=self._silence_off_image)

    def select_row(self, index):
        select_row(self.menu, index)

    def _clear_tree(self):
        self.menu.delete(*self.menu.get_children())

    def set_locale(self):
        self.music_little_label.config(text=_('music'))

        menu_children = self.menu.get_children()
        self.menu.item(menu_children[0], values=('', _('music')))
        self.menu.item(menu_children[1], values=('', _('favourites')))
        self.menu.item(menu_children[2], values=('', _('settings')))


def select_row(tree, index):
    tree_children = tree.get_children()[index]
    tree.focus(tree_children)
    tree.selection_set(tree_children)


class SongsView(View):
    def __init__(self, path, layout_name, master=None):
        super().__init__(path, master)
        self.ui = self.builder.get_object(layout_name, master)

        self.add_music_button = self.builder.get_object('addMusicButton')
        self.search_bar_input = tk.StringVar()
        self.search_bar = self.builder.get_object('searchBar')
        self.search_bar.configure(textvariable=self.search_bar_input)

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

        self.set_locale()

    def _generate_tree_style(self, name):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(name, background="#e8e9f2",
                        fieldbackground="#e8e9f2", foreground="black", borderwidth=0)
        style.map(name, background=[('selected', '#e2daf7')], foreground=[('selected', '#000000')])
        style.configure(name, rowheight=56)
        style.configure(name, font=('Yu Gothic UI Semilight', 14))

    def fill_tree(self, music_data):
        self._clear_tree()
        for index, (album_artist, duration, artwork) in enumerate(music_data):
            if artwork is None:
                self.songs_tree.insert('', 'end', values=('', album_artist, duration), iid='I' + str(index + 1))
            else:
                self.songs_tree.insert('', 'end', image=artwork, values=('', album_artist, duration),
                                       iid='I' + str(index + 1))

    def _clear_tree(self):
        self.songs_tree.delete(*self.songs_tree.get_children())

    def select_row(self, index):
        select_row(self.songs_tree, index)

    def set_locale(self):
        self.add_music_button.config(text=_('add music'))


class SettingsView(View):
    def __init__(self, path, layout_name, master=None):
        super().__init__(path, master)
        self.ui = self.builder.get_object(layout_name, master)
        self.settings_label = self.builder.get_object('settingsLabel')
        self.language_button_ru = self.builder.get_object('languageButtonRu')
        self.language_button_en = self.builder.get_object('languageButtonEn')
        self.set_locale()

    def set_locale(self):
        self.settings_label.config(text=_('settings'))
