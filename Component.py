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
        self.model = Model.AppModel(self.view)
        self.controller = Controller.AppController(self.view, self.model)
        components['app'] = self


class SongComponent(Component):
    def __init__(self, master_component):
        super().__init__()
        self.view = View.SongsView("resources/ui/songs_tree.ui", "songsFrame", master_component)
        self.model = Model.SongsModel(self.view)
        self.controller = Controller.SongController(self.view, self.model)
        components['song'] = self




class SettingsComponent(Component):
    def __init__(self):
        super().__init__()
        self.view = View.SettingsView("resources/ui/settings.ui", "songsFrame", components['app'].view.center_frame)
        self.model = Model.SettingsModel(self.view)
        self.controller = Controller.SettingsController(self.view, self.model)
        components['settings'] = self


def init_components():
    AppComponent()
    SongComponent(components['app'].view.center_frame)
    SettingsComponent()



def run():
    components['settings'].controller.hide_view()
    components['app'].view.main_window.mainloop()
