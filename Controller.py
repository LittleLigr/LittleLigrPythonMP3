from abc import ABCMeta
from tkinter.filedialog import askopenfilenames


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


class SongController(Controller):
    def __init__(self, view, model):
        super().__init__(view, model)
        self.view.addMusicButton['command'] = self._file_dialog
        self.view.songs_tree.bind("<Double-1>", self.treeClickEvent)

    def add_music_handler(self):
        filename = askopenfilenames(title='"pen')
        pass

    def _file_dialog(self):
        text_file_extensions = ['*.mp3', '*.flac', '*.ogg', '*.wma', '*.wav', '*.alac', '*.m4a', '*.aac']
        ftypes = [
            ('Music', text_file_extensions),
        ]
        filenames = askopenfilenames(title='"pen', filetypes=ftypes)

        for file in filenames:
            self.model.add_music(file)

        pass

    def treeClickEvent(self, event):
        item = self.view.songs_tree.selection()[0]
        print('id? ' + str(event.y))
        print("you clicked on", self.view.songs_tree.item(item,"values"))


class SettingsController(Controller):
    def __init__(self, view, model):
        super().__init__(view, model)
