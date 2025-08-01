from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from src.data.gutenberg.book_info import BookInfo, get_book_path
from src.data.utils import normalize

def save_books(dir: Path, books: List[BookInfo], *, max_workers: int|None = None) -> None:
    """Save a list of BookInfo objects to disk, grouped by author directory."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for book in books:
            author_dir = dir / (book.author or "unknown")
            author_dir.mkdir(parents=True, exist_ok=True)
            file_path = author_dir / get_book_path(book)
            futures.append(executor.submit(book.save, file_path))
        for future in as_completed(futures):
            future.result()

def load_books(root_dir: Path) -> list[BookInfo]:
    """Load all BookInfo objects from a given root directory."""
    if not root_dir.exists():
        raise FileNotFoundError(f"{root_dir} not found")
    book_paths: list[Path] = [
        path
        for author_dir in root_dir.iterdir()
        if author_dir.is_dir()
        for path in author_dir.glob("*.bin")
    ]
    books = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(BookInfo.load, path) for path in book_paths]
        for future in as_completed(futures):
            books.append(future.result())
    return books
