from abc import ABCMeta
from io import BytesIO

from PIL import Image, ImageTk
from tinydb import TinyDB
from tinytag import TinyTag

db = TinyDB("resources/data/music.json")


class Model:
    __metaclass__ = ABCMeta

    def __init__(self, view):
        self.view = view


class AppModel(Model):

    def __init__(self, app_view):
        super().__init__(app_view)


def _read_tag(path):
    tags = TinyTag.get(path, image=True)
    image_data = tags.get_image()

    image = None
    if image_data is not None:
        stream = BytesIO(image_data)
        image = ImageTk.PhotoImage(Image.open(stream).resize((50, 50)))

    return tags, image


def _prepare_view_fields(fields):
    duration_minutes = fields.duration / 60
    duration_seconds_part = int((duration_minutes - int(duration_minutes)) * 60)
    print(duration_seconds_part)
    duration = str(int(duration_minutes)) + "." + str(duration_seconds_part)
    print(fields)
    album_artist = fields.artist + ' - ' + fields.album

    return '', album_artist, duration


class SongsModel(Model):
    music = {}

    def __init__(self, songs_view):
        super().__init__(songs_view)
        for data in db:
            path = data.get('path')
            tags, image = _read_tag(path)

            self.music[path] = (tags, image)

            prepared_data = _prepare_view_fields(tags)
            self.view.insert(image, prepared_data)

    def add_music(self, path):
        if path not in self.music.keys():
            tags, image = _read_tag(path)
            self.music[path] = (tags, image)

            db.insert({'path': path})
            prepared_data = _prepare_view_fields(tags)
            self.view.insert(image, prepared_data)
            pass


class SettingsModel(Model):

    def __init__(self, settings_view):
        super().__init__(settings_view)
