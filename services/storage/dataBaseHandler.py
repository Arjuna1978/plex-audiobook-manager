import sqlite3
import os

class dataBaseHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(dataBaseHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_name="library.db"):
        if not hasattr(self, 'initialized'):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, db_name)
            self._init_db()
            self.initialized = True

    def _init_db(self):
        """
        Internal method to ensure the database schema exists.
        This effectively incorporates your initialization script.
        """
        with self.get_connection() as conn:
            # Using executescript to run your complete schema definition
            conn.executescript('''
            -- ==========================================
            -- BASE TABLES (No Foreign Key Dependencies)
            -- ==========================================

            CREATE TABLE IF NOT EXISTS CANNON (
                cannon_id TEXT PRIMARY KEY,
                title TEXT,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS SERVER (
                server_id TEXT PRIMARY KEY,
                plex_id TEXT,
                name TEXT,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS FILES (
                file_id TEXT PRIMARY KEY,
                file_path TEXT,
                file_size_bytes INTEGER,
                container TEXT,
                notes TEXT
            );

            CREATE TABLE IF NOT EXISTS GENRES (
                genre_id INTEGER PRIMARY KEY,
                genre_name TEXT,
                source_taxonomy TEXT,
                source_id TEXT,
                source_txt TEXT
            );

            CREATE TABLE IF NOT EXISTS TAGS (
                tag_id INTEGER PRIMARY KEY,
                tag_name TEXT,
                source_taxonomy TEXT,
                source_id TEXT,
                source_txt TEXT
            );

            -- ==========================================
            -- PRIMARY TABLES (With Foreign Key Constraints)
            -- ==========================================

            CREATE TABLE IF NOT EXISTS USERS (
                user_id TEXT PRIMARY KEY,
                name TEXT,
                light_mode INTEGER NOT NULL DEFAULT 1 CHECK (light_mode IN (0, 1)),
                file_id TEXT,
                FOREIGN KEY (file_id) REFERENCES FILES(file_id)
            );

            CREATE TABLE IF NOT EXISTS LIBRARIES (
                library_id TEXT PRIMARY KEY,
                name TEXT,
                type TEXT,
                server TEXT,
                path TEXT,
                plex_id TEXT,
                file_id TEXT,
                FOREIGN KEY (file_id) REFERENCES FILES(file_id)
            );

            CREATE TABLE IF NOT EXISTS CONTRIBUTORS (
                contributor_id TEXT PRIMARY KEY,
                plex_id TEXT,
                asin_id TEXT,
                asin_txt TEXT,
                name TEXT,
                type TEXT,
                description TEXT,
                links TEXT
            );

            CREATE TABLE IF NOT EXISTS SERIES (
                series_id TEXT PRIMARY KEY,
                cannon_id TEXT,
                title TEXT,
                notes TEXT,
                FOREIGN KEY (cannon_id) REFERENCES CANNON(cannon_id)
            );

            CREATE TABLE IF NOT EXISTS BOOKS (
                book_id TEXT PRIMARY KEY,
                plex_id TEXT,
                series_id TEXT,
                cannon_id TEXT,
                asin_id TEXT,
                asin_txt TEXT,
                isbn_id TEXT,
                library_id TEXT,
                title TEXT NOT NULL DEFAULT DEFAULT "UNKNOWN",
                duration TEXT,
                description TEXT NOT NULL DEFAULT DEFAULT "UNKNOWN",
                in_library INTEGER NOT NULL DEFAULT 0 CHECK (in_library IN (0, 1)),
                has_started INTEGER NOT NULL DEFAULT 0 CHECK (has_started IN (0, 1)),
                has_finished INTEGER NOT NULL DEFAULT 0 CHECK (has_started IN (0, 1)),
                publish_year INTEGER NOT NULL DEFAULT 1000,
                FOREIGN KEY (series_id) REFERENCES SERIES(series_id),
                FOREIGN KEY (cannon_id) REFERENCES CANNON(cannon_id),
                FOREIGN KEY (library_id) REFERENCES LIBRARIES(library_id)
            );

            CREATE TABLE IF NOT EXISTS CHAPTERS (
                chapter_id INTEGER PRIMARY KEY,
                plex_id TEXT,
                book_id TEXT,
                title TEXT,
                chapter_index_txt TEXT,
                chapter_index_number INTEGER,
                start_time_offset INTEGER,
                end_time_offset INTEGER,
                duration INTEGER GENERATED ALWAYS AS (end_time_offset - start_time_offset),
                have_listened INTEGER,
                FOREIGN KEY (book_id) REFERENCES BOOKS(book_id)
            );

            -- ==========================================
            -- MAPPING TABLES (Many-to-Many Relationships)
            -- ==========================================

            CREATE TABLE IF NOT EXISTS BOOK_FILES_MAP (
                id INTEGER PRIMARY KEY,
                book_id TEXT,
                file_id TEXT,
                description TEXT,
                FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
                FOREIGN KEY (file_id) REFERENCES FILES(file_id)
            );
            
            CREATE TABLE IF NOT EXISTS USER_SERVER_MAP (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                server_id TEXT,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES USERS(user_id),
                FOREIGN KEY (server_id) REFERENCES SERVER(server_id)
            );
                               
            CREATE TABLE IF NOT EXISTS LIBRARY_SERVER_MAP (
                id INTEGER PRIMARY KEY,
                library_id TEXT,
                server_id TEXT,
                description TEXT,
                FOREIGN KEY (library_id) REFERENCES LIBRARIES(library_id),
                FOREIGN KEY (server_id) REFERENCES SERVER(server_id)
            );


            CREATE TABLE IF NOT EXISTS SERIES_FILES_MAP (
                id INTEGER PRIMARY KEY,
                series_id TEXT,
                file_id TEXT,
                description TEXT,
                FOREIGN KEY (series_id) REFERENCES SERIES(series_id),
                FOREIGN KEY (file_id) REFERENCES FILES(file_id)
            );

            CREATE TABLE IF NOT EXISTS CANNON_FILES_MAP (
                id INTEGER PRIMARY KEY,
                cannon_id TEXT,
                file_id TEXT,
                description TEXT,
                FOREIGN KEY (cannon_id) REFERENCES CANNON(cannon_id),
                FOREIGN KEY (file_id) REFERENCES FILES(file_id)
            );

            CREATE TABLE IF NOT EXISTS CONTRIBUTOR_FILES_MAP (
                id INTEGER PRIMARY KEY,
                contributor_id TEXT,
                file_id TEXT,
                description TEXT,
                FOREIGN KEY (contributor_id) REFERENCES CONTRIBUTORS(contributor_id),
                FOREIGN KEY (file_id) REFERENCES FILES(file_id)
            );

            CREATE TABLE IF NOT EXISTS BOOK_CONTRIBUTOR_MAP (
                id INTEGER PRIMARY KEY,
                book_id TEXT,
                contributor_id TEXT,
                FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
                FOREIGN KEY (contributor_id) REFERENCES CONTRIBUTORS(contributor_id)
            );


            CREATE TABLE IF NOT EXISTS BOOK_GENRE_MAP (
                id INTEGER PRIMARY KEY,
                book_id TEXT,
                genre_id INTEGER,
                FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
                FOREIGN KEY (genre_id) REFERENCES GENRES(genre_id)
            );

            CREATE TABLE IF NOT EXISTS BOOK_TAG_MAP (
                id INTEGER PRIMARY KEY,
                book_id TEXT,
                tag_id INTEGER,
                FOREIGN KEY (book_id) REFERENCES BOOKS(book_id),
                FOREIGN KEY (tag_id) REFERENCES TAGS(tag_id) 
            );

            CREATE TABLE IF NOT EXISTS CONTRIBUTOR_GENRE_MAP ( 
                id INTEGER PRIMARY KEY,
                contributor_id TEXT, -- Corrected column
                genre_id INTEGER,
                FOREIGN KEY (contributor_id) REFERENCES CONTRIBUTORS(contributor_id), 
                FOREIGN KEY (genre_id) REFERENCES GENRES(genre_id)
            );

            CREATE TABLE IF NOT EXISTS CONTRIBUTOR_TAG_MAP ( 
                id INTEGER PRIMARY KEY,
                contributor_id TEXT,
                tag_id INTEGER,
                FOREIGN KEY (contributor_id) REFERENCES CONTRIBUTORS(contributor_id),
                FOREIGN KEY (tag_id) REFERENCES TAGS(tag_id)
            );
            ''')
# CRUD opperations

    def create_record(self, table, data):
        """
        Create/Update: add another recort (row) to your table}.
        Args:
        table: Which table you want to add to
        data: the row data in the from of a dict
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join([':' + k for k in data.keys()])
        query = f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})"
        with self.get_connection() as conn:
            conn.execute(query, data)
            conn.commit()

    def get_record_by_field(self, table, column, value):
        """
        Fetch a record based on any column and value
        
        Args:
        Table: The table to trget
        Column: The Column to search in
        Value: The Value to serach for
        """
        query = f"SELECT * FROM {table} WHERE {column} = ?"
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row 
            return conn.execute(query, (value,)).fetchone()

    def delete_recorf_by_field(self, table, field, value):
        """
        Delete a record based on any column and value
        
        Args:
        Table: The table to trget
        Column: The Column to search in
        Value: The Value to serach for
        """
        query = f"DELETE FROM {table} WHERE {field} = ?"
        with self.get_connection() as conn:
            conn.execute(query, (value,))
            conn.commit()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_field_by_xLookup(self, table, target_column, search_column, search_value):
        """Fetch a specific value by a searchable column."""
        query = f"SELECT {target_column} FROM {table} WHERE {search_column} = ?"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (search_value,))
            row = cursor.fetchone()
            return row[0] if row else None
    
    def change_field_by_xLookup(self, table, target_column, new_value, search_column, search_value):
        """Change a specific field based on a lookup condition."""
        query = f"UPDATE {table} SET {target_column} = ? WHERE {search_column} = ?"
        
        with self.get_connection() as conn:
            conn.execute(query, (new_value, search_value))
            conn.commit()