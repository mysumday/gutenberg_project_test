## Project Structure

```
├── configs/                        # Configuration files
├── data/                           # Local storage for books and datasets
├── scripts/                        # Scripts for training, transformation, etc.
└── src/                            # Core source code
```

---
### configs/

* `gutenberg_config.yaml`: Stores paths and parameters used across the pipeline.

---

### data/
* `books/`: Binary representations of downloaded books, organized by author.
* `data_sets/`: CSV files representing processed datasets ready for modeling.

---

### scripts/

* Currently empty, but reserved for scripts that handle end-to-end execution

---

### src/

Main Python source modules.

#### config/

* `configuration.py`:

  * `GutenbergConfig`: Loads and provides access to YAML configuration settings.

#### data/gutenberg/

* `book_info.py`:

  * `BookInfo`: Represents a book retrieved from the Gutendex API.
      * `id`: Gutenberg ID with validation.
      * `author`: Normalized main author name.
      * `title`: Normalized title.
      * `url`: Download URL for plain text.
      * `text`: Cleaned main body of the book, extracted using configured start/end markers.
    * Methods:
      * `_get_book_text()`: Isolates the main content from raw download.
      * `_get_url_response()`: Requests metadata from Gutendex API.
      * `save()`, `load()`: Serialize/deserialize BookInfo objects with joblib.

	  * `get_book_path(book: BookInfo) -> str`: Generates a standardized filename from a book title.

* `fetch.py`:

  * `get_books(ids: list[int]) -> list[BookInfo]`: Fetches books using their Gutenberg IDs.
  * `get_books_by_author(authors: list[str]) -> list[BookInfo]`: Retrieves books by author name(s).

* `storage.py`:

  * `save_books(dir, books, *, max_workers)`: Saves books to disk grouped by author.
  * `load_books(root_dir)`: Loads books from local storage.

#### utils.py

Utility functions for normalization and directory structure handling:

* `get_by_part_key(d, k)`: Partial key match dictionary lookup.
* `normalize(text)`: Lowercases and replaces delimiters with underscores.
* `get_auth_from_dir(root_dir)`: Lists normalized author directories.
* `chunk_text(text, chunk_size=500, overlap=100)`: Splits text into overlapping chunks.

---

### features/

* `features.py`: High-level feature orchestration.

  * `extract_features(raw_text, features=None)`: Extracts selected linguistic features from text.
  * `build_feature_dataset(books, features=None, split_text=True)`: Constructs a DataFrame of features from books.
  * `Features (Enum)`: Enum for lexical, stylometric, syntactic, etc.

---

### models/

* `cluster_data(df, n_clusters, random_state, perplexity)`:
  Clusters feature data using KMeans and visualizes using t-SNE.

---

### plots/

* `plot_author_feature_distributions(df, aggregate="mean")`:
  Creates bar and violin plots for feature distributions by author.

* `plot_clusters(result_df)`:
  Plots 2D t-SNE results with clusters and author labels.

---

## How To Use (WIP)

* Fetching books from Gutenberg.
* Extracting features.
* Clustering authors based on style.
* Visualizing author space.