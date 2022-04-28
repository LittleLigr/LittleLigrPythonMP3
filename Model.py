from io import BytesIO

from PIL import Image, ImageTk
from tinydb import TinyDB, Query, where
from tinytag import TinyTag
import pygame


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
    return album_artist, duration


class MusicManager:
    _music_db = TinyDB("resources/data/music.json")
    _app_db = TinyDB("resources/data/app.json")
    _shown_music_index = -1
    _shown_music_data = None
    _playing_music_data = None
    _music = {}
    _current_music = {}
    _current_filter = ''
    _app_view = None
    _song_view = None
    _pause = True

    _silence = False
    _volume = 0

    def init(self, app_view, song_view):
        self._app_view = app_view
        self._song_view = song_view
        pygame.init()
        self.upload_and_show_music_from_db()
        self._upload_app_settings()

    def next(self):
        if self._shown_music_index + 1 >= len(self._current_music):
            self._select_shown(0)
        else:
            self._select_shown(self._shown_music_index + 1)

        self._song_view.select_row(self._shown_music_index)
        self._fill_music_bar()

    def previous(self):
        if self._shown_music_index - 1 < 0:
            self._select_shown(len(self._current_music) - 1)
        else:
            self._select_shown(self._shown_music_index - 1)

        self._song_view.select_row(self._shown_music_index)
        self._fill_music_bar()

    def switch_shown_music(self, index):
        self._select_shown(index)
        self._song_view.select_row(self._shown_music_index)
        self._fill_music_bar()

    def add_music(self, path):
        self._music_db.insert({'path': path, 'favourite': False})
        self.upload_music(path, False)
        self.filter(self._current_filter)

    def _fill_music_bar(self):
        self._app_view.fill_music_bar(self._shown_music_data[0].album,
                                      self._shown_music_data[0].artist,
                                      self._shown_music_data[1],
                                      self._shown_music_data[3],
                                      self._shown_music_data == self._playing_music_data,
                                      self._pause)

    def upload_music(self, path, favourite):
        tags, image = _read_tag(path)
        prepared_data = _prepare_view_fields(tags)
        self._music[path] = (tags, image, prepared_data, favourite)
        return self._music[path]

    def clear(self):
        self._music.clear()

    def filter(self, filter_seq):
        self._current_filter = filter_seq
        if filter_seq is not '':
            self._current_music.clear()
            for path, music_data in self._music.items():
                tags = music_data[0]
                is_match = str(tags.album).__contains__(filter_seq)
                is_match = is_match or str(tags.artist).__contains__(filter_seq)
                is_match = is_match or str(tags.genre).__contains__(filter_seq)
                is_match = is_match or str(tags.year).__contains__(filter_seq)
                if is_match:
                    self._current_music[path] = music_data
        else:
            self._current_music = self._music.copy()

        self._song_view.fill_tree(self._prepare_music_data())
        self.select(0)

    def _prepare_music_data(self):
        music_data_list = []
        for index, data in enumerate(self._current_music.values()):
            music_data_list.append((data[2][0], data[2][1], data[1]))

        return music_data_list

    def _contains(self, path):
        return path in self._current_music.keys()

    def _get_data_by_id(self, index):
        return list(self._current_music.values())[index]

    def _get_path_by_id(self, index):
        return list(self._current_music.keys())[index]

    def favourite(self):
        path = self._get_path_by_id(self._shown_music_index)
        data = Query()
        music_data = self._music_db.search(data.path == path).__getitem__(0)
        self._music_db.update({'favourite': not music_data.get('favourite')}, data.path == path)
        self._music[path] = (self._music[path][0],
                             self._music[path][1],
                             self._music[path][2],
                             not self._music[path][3])

        self.filter(self._current_filter)
        self._fill_music_bar()

    def delete(self):
        path = self._get_path_by_id(self._shown_music_index)
        self._music_db.remove(where('path') == path)
        self._music.pop(path)
        self._current_music.pop(path)
        self.filter(self._current_filter)

    def select(self, index):
        if index < len(self._current_music.values()):
            self._select_shown(index)
            self._fill_music_bar()
            self._song_view.select_row(index)
        else:
            self._select_shown(-1)
            self._app_view.hide_music_bar()

    def _select_shown(self, index):
        if index == -1:
            self._shown_music_index = -1
            self._shown_music_data = None
        else:
            self._shown_music_index = index
            self._shown_music_data = self._get_data_by_id(index)

    def play_reaction(self):
        if self._shown_music_data != self._playing_music_data:
            self._play_music()
            self._pause = False
        else:
            if self._pause:
                pygame.mixer.music.unpause()
                self._pause = False
            else:
                pygame.mixer.music.pause()
                self._pause = True

        self._fill_music_bar()

    def _play_music(self):
        self._playing_music_data = self._shown_music_data
        music_path = list(self._current_music.keys())[self._shown_music_index:]
        if len(music_path) > 0:
            [pygame.mixer.music.load(path) for path in music_path.__reversed__()]
            pygame.mixer.music.play()

    def upload_and_show_music_from_db(self):
        for data in self._music_db:
            path = data.get('path')
            favourite = data.get('favourite')
            self.upload_music(path, favourite)
        self.filter("")

    def set_volume(self, volume):
        self._app_db.update({'volume': volume})
        self._app_view.set_volume_bar_value(volume)
        self._volume = volume
        pygame.mixer.music.set_volume(volume / 100)
        if volume > 0:
            self._silence = False

    def _upload_app_settings(self):
        default = self._app_db.all()[0]
        volume = default['volume']
        self.set_volume(volume)

    def silence(self):
        if self._silence:
            self._app_view.set_volume_bar_value(self._volume)
            pygame.mixer.music.set_volume(self._volume / 100)
        else:
            self._app_view.set_volume_bar_value(0)
            pygame.mixer.music.set_volume(0)
        self._silence = not self._silence


music_manager = MusicManager()
