import json
import logging
from datetime import datetime
from pathlib import Path

from configuration.main import Configuration
from dto import Coordinates, Point, Size, Tile
from errors import BaseAppError

log = logging.getLogger(__name__)


class ConfigurationLoadError(BaseAppError):
    pass


class ConfigurationFileStorageHandler:
    @staticmethod
    def _get_save_dir() -> Path:
        """Presumes that application is run from root project dir."""
        return Path.joinpath(Path.cwd(), 'save')

    def _ensure_save_dir_exists(self) -> Path:
        save_dir = self._get_save_dir()
        if not Path.is_dir(save_dir):
            Path.mkdir(save_dir)
        return save_dir

    def _resolve_file(self, file_name: str) -> Path:
        filename_path = Path(file_name)
        file_path = Path.resolve(filename_path)
        if not Path.is_file(file_path):
            file_path = Path.joinpath(self._get_save_dir(), filename_path)
            if not Path.is_file(file_path):
                raise ConfigurationLoadError(f'File "{file_name}" not found.')

        return file_path

    def save(self, config: Configuration) -> None:
        """Save map and surface to "cwd/save" dir."""
        save_dir_path = self._ensure_save_dir_exists()

        serialized_map = []
        for row in config.map:
            serialized_map.append([tile.serialize() for tile in row])

        file_path = save_dir_path.joinpath(f'{datetime.now().date().isoformat()}-scale-{config.map_scale}.conf')
        with file_path.open('w') as config_file:
            json.dump({
                'surface': config.surface,
                'map': serialized_map,
                'scale': config.map_scale,
                'actor_on_map_pos': config.actor_on_map_pos.serialize(),
                'actor_scene_center_offset': config.actor_scene_center_offset.serialize(),
                'scene_on_map_coords': config.scene_on_map_coords.serialize(),
                'scene_is_most_top': config.scene_is_most_top,
                'scene_is_most_bottom': config.scene_is_most_bottom,
                'scene_is_most_right': config.scene_is_most_right,
                'scene_is_most_left': config.scene_is_most_left,
            },
                fp=config_file,
                sort_keys=True,
                indent=None,
            )

            message = 'Config saved.'
            log.info(message)
            config.messages.append(message)

    def load(self, config: Configuration, file_name: str) -> None:
        file_path = self._resolve_file(file_name)

        try:
            with file_path.open('r') as config_file:
                data = json.load(fp=config_file)

                scale = data['scale']
                if scale != config.map_scale:
                    error_text = f'Map and screen resolution scales mismatch. ' \
                                 f'You try to load map with scale {scale} ' \
                                 f'on screen with scale {config.map_scale}.'
                    log.error(error_text)
                    raise ConfigurationLoadError(error_text)

                serialized_map = data['map']
                actor_on_map_pos = Point(**data['actor_on_map_pos'])
                actor_scene_center_offset = Size(**data['actor_scene_center_offset'])
                serialized_scene_on_map_coords = data['scene_on_map_coords']
                scene_is_most_top = data['scene_is_most_top']
                scene_is_most_bottom = data['scene_is_most_bottom']
                scene_is_most_right = data['scene_is_most_right']
                scene_is_most_left = data['scene_is_most_left']

        except KeyError as error:
            raise ConfigurationLoadError('Invalid file.') from error
        except json.JSONDecodeError as error:
            raise ConfigurationLoadError('Unable to decode file content.') from error

        parsed_map = []
        for row in serialized_map:
            parsed_map.append([Tile(**tile) for tile in row])

        scene_on_map_coords = Coordinates(
            **{key: Point(**value) for key, value in serialized_scene_on_map_coords.items()}
        )

        # Restores map
        config.map = parsed_map
        config.surface = data['surface']

        # Restores actor position
        config.actor_on_map_pos = actor_on_map_pos
        config.actor_scene_center_offset = actor_scene_center_offset
        config.scene_on_map_coords = scene_on_map_coords
        config.scene_is_most_top = scene_is_most_top
        config.scene_is_most_bottom = scene_is_most_bottom
        config.scene_is_most_right = scene_is_most_right
        config.scene_is_most_left = scene_is_most_left
