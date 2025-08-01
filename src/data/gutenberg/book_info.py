from functools import cached_property
from typing import Any, Self
import requests
import joblib
from pathlib import Path
from src.config.configuration import GutenbergConfig
from src.data.utils import get_by_part_key, normalize

class BookInfo:
    """Represents a single book fetched from Project Gutenberg via its Gutendex API."""
    _CONFIG = GutenbergConfig()
    
    def __init__(self, id: int) -> None:
        self.id = id
        self._author = None
        self._title = None
        self._url = None
        self._text = None
        self._raw_book_info: dict[str, Any] = self._get_url_response().json()


    def __repr__(self) -> str:
        return f"Book: {self.title} by {self.author}"

    @property
    def id(self) -> int:
        """The Gutenberg ID of the book."""
        return self._id

    @id.setter
    def id(self, n: int) -> None:
        if n <= 0:
            raise ValueError(f"Id of the book must a a positive number and got {n}")
        self._id = n

    @property
    def author(self) -> str | None:
        if self._author is None:
            authors: list[dict[str, str]] | None = self._raw_book_info.get("authors")
            if not authors:
                return None
            main_author = authors[0].get("name")
            self._author = normalize(main_author) if main_author else None
        return self._author

    @property
    def title(self) -> str | None:
        if self._title is None:
            title = self._raw_book_info.get("title")
            self._title = normalize(title) if title else None
        return self._title

    @property
    def url(self) -> str | None:
        """Returns the download URL for the plain text version of the book."""
        if self._url is None:
            all_urls: dict[str, str] | None = self._raw_book_info.get("formats")
            if all_urls is None:
                return None
            self._url = get_by_part_key(all_urls, self._CONFIG.text_tag)
        return self._url

    @cached_property
    def text(self) -> str | None:
        """Returns the full cleaned text of the book, between configured START and END markers."""
        return self._get_book_text(self.url) if self.url else None


    def _get_book_text(self, book_url: str) -> str | None:
        """Fetch the book content and extract only the main body using markers."""
        try:
            resp = requests.get(book_url)
            resp.raise_for_status()
            body = resp.text
        except Exception as e:
            print(f"Could not retrieve text of the book. {e}")
            return None
        
        try:
            text = body.split(self._CONFIG.start_marker, maxsplit=1)[-1]
            text = text.split(self._CONFIG.end_marker, maxsplit=1)[0]
            return text.strip()
        except Exception as e:
            print(f"Text has incorrect fromat unable to separate markers. {e}")
            return None

    def _get_url_response(self) -> requests.Response:
        """Send request to Gutendex API to retrieve metadata for this book."""
        url = self._CONFIG.gutenberg_url + str(self.id)
        response = requests.get(url)
        response.raise_for_status()  
        return response

    def save(self, path: Path) -> None:
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: Path) -> Self:
        return joblib.load(path)

def get_book_path(book: BookInfo, /) -> str:
    """Generate a standardized filename for a book based on its title."""
    return f"{normalize(book.title or 'untitled')}.bin"