from abc import ABCMeta

import Controller
import Model
import View


components = {}


class Component:
    __metaclass_ = ABCMeta

    def __init__(self):
        self.view = None
        self.controller = None
        self.model = None


class AppComponent(Component):
    def __init__(self):
        super().__init__()
        self.view = View.AppView("resources/ui/main.ui", "mainFrame")
        self.controller = Controller.AppController(self.view)
        components['app'] = self


class SongComponent(Component):
    def __init__(self, master_component):
        super().__init__()
        self.view = View.SongsView("resources/ui/songs_tree.ui", "songsFrame", master_component)
        self.controller = Controller.SongController(self.view)
        components['song'] = self


class SettingsComponent(Component):
    def __init__(self, master_component):
        super().__init__()
        self.view = View.SettingsView("resources/ui/settings.ui", "songsFrame", master_component)
        self.controller = Controller.SettingsController(self.view)
        components['settings'] = self


def init_components():
    app = AppComponent()
    songs = SongComponent(app.view.center_frame)
    SettingsComponent(app.view.center_frame)
    Model.music_manager.init(app.view, songs.view)


def run():
    components['settings'].controller.hide_view()
    components['app'].view.main_window.mainloop()



