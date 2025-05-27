# Articles Management System

A simple Python project for managing authors, magazines, and articles using SQLite. This project demonstrates basic CRUD operations, object-relational mapping, and relationships between models.

## Features

- Manage Authors, Magazines, and Articles
- SQLite database with schema and seed data
- Python classes for each model with validation
- Query methods for searching and relationships
- Debug console for interactive exploration
- Unit test structure (expandable)

## Project Structure

```
lib/
  db/
    connection.py      # Database connection logic
    schema.sql         # Database schema (tables)
    seed.py            # Seed sample data
  models/
    author.py          # Author model
    magazine.py        # Magazine model
    articles.py        # Article model
    __init__.py        # Model imports
  debug.py             # Debug console for interactive testing
scripts/
  setup_db.py          # (To be implemented) Setup database
  run_queries.py       # (To be implemented) Example queries
README.md              # Project documentation
Pipfile                # Python dependencies
```

## Setup Instructions

### 1. Clone the repository from GitHub

```bash
git clone https://github.com/BrianSila/Articles-
cd Articles
```

### 2. Install dependencies (if using pipenv):

```bash
pipenv install
pipenv shell
pipenv install ipython  # For enhanced interactive debug console
```

Or use `pip install` as needed:

```bash
pip install pytest ipython
```

### 3. Initialize the database:

```bash
sqlite3 articles.db < lib/db/schema.sql
python -m lib.db.seed
```

### 4. Run the debug console:

```bash
python lib/debug.py
```

This opens an interactive shell with access to the models and database.

## Usage

- Use the model classes (`Author`, `Magazine`, `Article`) to create, update, and query data.
- Explore relationships (e.g., `author.articles()`, `magazine.contributers()`).
- Extend the test files in `tests/` for unit testing.

## Database Schema

- **authors**: id, name
- **magazines**: id, name, category
- **articles**: id, title, author_id, magazine_id

## Notes

- All database logic uses SQLite and Python's `sqlite3` module.
- The debug console loads sample data if the database is empty.
- The project is modular and easy to extend.

## License

MIT License
