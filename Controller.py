from abc import ABCMeta


class Controller:
    __metaclass__ = ABCMeta

    def __init__(self, view):
        self.view = view
        pass

    def hide_view(self):
        self.view.ui.pack_forget()

    def show_view(self, expand, fill):
        self.view.pack(expand=expand, fill=fill)


class AppController(Controller):
    def __init__(self, view):
        super().__init__(view)


class SongController(Controller):
    def __init__(self, view):
        super().__init__(view)


class SettingsController(Controller):
    def __init__(self, view):
        super().__init__(view)
