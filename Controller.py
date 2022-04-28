from abc import ABCMeta
from tkinter.filedialog import askopenfilenames

import Model


class Controller:
    __metaclass__ = ABCMeta

    def __init__(self, view):
        self.view = view

    def hide_view(self):
        self.view.ui.pack_forget()

    def show_view(self, expand, fill):
        self.view.pack(expand=expand, fill=fill)


class AppController(Controller):

    def __init__(self, view):
        super().__init__(view)
        self.view.play_button['command'] = Model.music_manager.play_reaction
        self.view.next_song_button['command'] = Model.music_manager.next
        self.view.previous_song_button['command'] = Model.music_manager.previous
        self.view.favourite_button['command'] = Model.music_manager.favourite
        self.view.delete_button['command'] = Model.music_manager.delete
        self.view.sound_bar.bind("<ButtonRelease-1>", self._set_volume)
        self.view.volume_button['command'] = Model.music_manager.silence

    def _set_volume(self, event):
        Model.music_manager.set_volume(self.view.sound_bar.get())
        pass


class SongController(Controller):

    def __init__(self, view):
        super().__init__(view)
        self.view.add_music_button['command'] = self._file_dialog
        self.view.songs_tree.bind("<ButtonRelease-1>", self.tree_click_event)
        self.view.search_bar.bind("<KeyRelease>", self.search_bar_event)

    def _file_dialog(self):
        text_file_extensions = ['*.mp3', '*.flac', '*.ogg', '*.wma', '*.wav', '*.alac', '*.m4a', '*.aac']
        types = [('Music', text_file_extensions)]
        filenames = askopenfilenames(title='"pen', filetypes=types)
        for file in filenames:
            Model.music_manager.add_music(file.replace('/', '\\'))

    def tree_click_event(self, event):
        Model.music_manager.switch_shown_music(self._get_selected_item())

    def search_bar_event(self, event):
        Model.music_manager.filter(self.view.search_bar_input.get())

    def _get_selected_item(self):
        item = self.view.songs_tree.selection()[0]
        return int(str(item)[1:])


class SettingsController(Controller):
    def __init__(self, view):
        super().__init__(view)
