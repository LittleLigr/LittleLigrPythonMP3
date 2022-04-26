from abc import ABCMeta
from tkinter.filedialog import askopenfilenames

import Component
import Model
from Model import music


class Controller:
    __metaclass__ = ABCMeta

    def __init__(self, view, model):
        self.view = view
        self.model = model
        pass

    def hide_view(self):
        self.view.ui.pack_forget()

    def show_view(self, expand, fill):
        self.view.pack(expand=expand, fill=fill)


class AppController(Controller):
    def __init__(self, view, model):
        super().__init__(view, model)
        self.view.play_button['command'] = self.play_music

    def play_music(self):
        import pygame
        pygame.init()

        pygame.mixer.music.load(Model.selected_music_path)
        pygame.mixer.music.play()


class SongController(Controller):
    def __init__(self, view, model):
        super().__init__(view, model)
        self.view.addMusicButton['command'] = self._file_dialog
        self.view.songs_tree.bind("<Double-1>", self.treeClickEvent)

    def _file_dialog(self):
        text_file_extensions = ['*.mp3', '*.flac', '*.ogg', '*.wma', '*.wav', '*.alac', '*.m4a', '*.aac']
        types = [('Music', text_file_extensions)]
        filenames = askopenfilenames(title='"pen', filetypes=types)

        for file in filenames:
            self.model.add_music(file.replace('/', '\\'))

        pass

    def treeClickEvent(self, event):
        item = self.view.songs_tree.selection()[0]
        Model.selected_music_path = self.view.songs_tree.item(item, "text")
        fields_data = music[Model.selected_music_path]
        tags = fields_data[0]
        image = fields_data[1]

        app_component = Component.components['app']
        app_component.view.fill_music_bar(tags.artist, tags.album, image)
        pass


class SettingsController(Controller):
    def __init__(self, view, model):
        super().__init__(view, model)
