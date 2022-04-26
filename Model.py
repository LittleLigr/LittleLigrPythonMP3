from abc import ABCMeta
from io import BytesIO

from PIL import Image, ImageTk
from tinydb import TinyDB
from tinytag import TinyTag

import Component

db = TinyDB("resources/data/music.json")
music = {}
selected_music_path = ""


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
        artwork = Image.open(stream)

        if artwork.width > artwork.height:
            ratio = artwork.height / artwork.width
            x, y = 50, 50 * ratio
        else:
            ratio = artwork.width / artwork.height
            x, y = 50 * ratio, 50

        image = ImageTk.PhotoImage(artwork.resize((int(x), int(y))))

    return tags, image


def _prepare_view_fields(fields):
    duration_minutes = fields.duration / 60
    duration_seconds_part = int((duration_minutes - int(duration_minutes)) * 60)
    duration = str(int(duration_minutes)) + "." + str(duration_seconds_part)
    album_artist = fields.artist + ' - ' + fields.album

    return '', album_artist, duration


class SongsModel(Model):

    def __init__(self, songs_view):
        super().__init__(songs_view)

    def upload_music(self):
        for data in db:
            path = data.get('path')
            tags, image = _read_tag(path)
            prepared_data = _prepare_view_fields(tags)
            music[path] = (tags, image)
            self.view.insert(image, path, prepared_data)

        if len(music) > 0:
            first_item = self.view.songs_tree.get_children()[0]
            self.view.songs_tree.focus(first_item)
            self.view.songs_tree.selection_set(first_item)

            Component.components['song'].controller.treeClickEvent(None)

    def add_music(self, path):
        if path not in music.keys():
            tags, image = _read_tag(path)
            music[path] = (tags, image)

            db.insert({'path': path})
            prepared_data = _prepare_view_fields(tags)
            self.view.insert(image, path, prepared_data)
            pass


class SettingsModel(Model):

    def __init__(self, settings_view):
        super().__init__(settings_view)
