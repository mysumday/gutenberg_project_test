from concurrent.futures import ThreadPoolExecutor, as_completed
from src.data.gutenberg.book_info import BookInfo

def get_books(ids: list[int]) -> list[BookInfo]:
    """Concurrently fetch and construct BookInfo objects from a list of Gutenberg book IDs."""
    books = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(BookInfo, id_) for id_ in ids]
        for future in as_completed(futures):
            book = future.result()
            print(f"Book loaded: {book}")
            books.append(book)
    return books


def get_books_by_author(authors: list[str]) -> list[BookInfo]:
    books = []
    for author in authors:
        if author not in BookInfo._CONFIG.authors:
            # ADD: exception handling
            continue
        books.extend(get_books(BookInfo._CONFIG.authors[author]))
    return books
        