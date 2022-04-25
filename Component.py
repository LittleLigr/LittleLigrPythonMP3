import Controller
import Model
import View

components = {}


class Component:
    def __init__(self):
        self.view = None
        self.controller = None
        self.model = None


class AppComponent(Component):
    def __init__(self):
        super().__init__()
        self.view = View.AppView("resources/ui/main.ui", "mainFrame")
        self.controller = Controller.AppController(self.view)
        self.model = Model.AppModel(self.view)
        components['app'] = self


class SongComponent(Component):
    def __init__(self):
        super().__init__()
        self.view = View.SongsView("resources/ui/songs_tree.ui", "songsFrame", components['app'].view.center_frame)
        self.controller = Controller.SongController(self.view)
        self.model = Model.SongsModel(self.view)
        components['song'] = self


class SettingsComponent(Component):
    def __init__(self):
        super().__init__()
        self.view = View.SettingsView("resources/ui/settings.ui", "songsFrame", components['app'].view.center_frame)
        self.controller = Controller.SettingsController(self.view)
        components['settings'] = self


def init_components():
    AppComponent()
    SongComponent()
    SettingsComponent()


def run():
    components['settings'].controller.hide_view()
    components['app'].view.main_window.mainloop()
