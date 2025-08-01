import yaml
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_PATH = Path.cwd() / "configs/gutenberg_config.yaml"


class GutenbergConfig:
    """
    Loads and provides access to the Gutenberg project configuration from a YAML file.
    """
    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            self._config = yaml.safe_load(f)

    @property
    def gutenberg_url(self) -> str:
        return self._config["GUTENBERG"]["URL"]

    @property
    def text_tag(self) -> str:
        return self._config["GUTENBERG"]["TEXT_TAG"]

    @property
    def start_marker(self) -> str:
        return self._config["GUTENBERG"]["START_MARKER"]

    @property
    def end_marker(self) -> str:
        return self._config["GUTENBERG"]["END_MARKER"]

    @property
    def authors(self) -> dict[str, list[int]]:
        return self._config["AUTHORS"]

    def get_books_by_author(self, author: str) -> list[int]:
        try:
            return self.authors[author]
        except KeyError:
            raise ValueError(f"Author '{author}' not found in config")

    def __getitem__(self, key: str) -> Any:
        return self._config[key]