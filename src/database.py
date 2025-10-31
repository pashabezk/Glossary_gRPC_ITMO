import sqlite3
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any

DATABASE_DIR = Path(__file__).resolve().parent.parent / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH = DATABASE_DIR / "glossary.db"


def get_db_connection():
	"""Establishes a connection to the database."""
	conn = sqlite3.connect(DATABASE_PATH)
	conn.row_factory = sqlite3.Row
	return conn


def init_db():
	"""Initializes the database and creates the terms table if it doesn't exist."""
	try:
		with get_db_connection() as conn:
			cursor = conn.cursor()
			cursor.execute(
				'''
					CREATE TABLE IF NOT EXISTS terms (
						term TEXT PRIMARY KEY NOT NULL,
						definition TEXT NOT NULL
					)
				'''
			)
			conn.commit()
		logging.info("Database initialized successfully.")
	except sqlite3.Error as e:
		logging.error(f"Database initialization failed: {e}")
		raise


def add_term(term_data: Dict[str, str]) -> Dict[str, str]:
	"""Adds a new term to the database."""
	with get_db_connection() as conn:
		conn.execute(
			"INSERT INTO terms (term, definition) VALUES (?, ?)",
			(term_data['term'], term_data['definition'])
		)
		conn.commit()
	logging.info(f"Added term: {term_data['term']}")
	return term_data


def get_term(term_str: str) -> Optional[Dict[str, str]]:
	"""Retrieves a single term by its name."""
	with get_db_connection() as conn:
		term_row = conn.execute("SELECT * FROM terms WHERE term = ?", (term_str,)).fetchone()
	if term_row:
		logging.info(f"Retrieved term: {term_str}")
		return dict(term_row)
	logging.warning(f"Term not found: {term_str}")
	return None


def get_all_terms() -> List[Dict[str, str]]:
	"""Retrieves all terms from the database."""
	with get_db_connection() as conn:
		terms = conn.execute("SELECT * FROM terms ORDER BY term").fetchall()
	logging.info(f"Retrieved {len(terms)} terms.")
	return [dict(term) for term in terms]


def update_term(term: str, new_definition: str) -> int:
	"""Updates an existing term. Returns the number of rows affected."""
	with get_db_connection() as conn:
		cursor = conn.cursor()
		cursor.execute(
			"UPDATE terms SET definition = ? WHERE term = ?",
			(new_definition, term)
		)
		conn.commit()
		logging.info(f"Updated term: {term}")
		return cursor.rowcount


def delete_term(term: str) -> int:
	"""Deletes a term by its name. Returns the number of rows affected."""
	with get_db_connection() as conn:
		cursor = conn.cursor()
		cursor.execute("DELETE FROM terms WHERE term = ?", (term,))
		conn.commit()
		logging.info(f"Deleted term: {term}")
		return cursor.rowcount
