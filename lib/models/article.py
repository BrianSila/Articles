import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from db.connection import get_connection

class Article:
    
    def __init__(self, title, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f"Article(id={self.id}, title='{self.title}', author_id={self.author_id}, magazine_id={self.magazine_id})"

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or len(value) < 5:
            raise ValueError("Title must be a string of at least 5 characters")
        self._title = value

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        if self.id is None: 
            cursor.execute(
                """INSERT INTO articles (title, author_id, magazine_id) 
                VALUES (?, ?, ?) RETURNING id""",
                (self.title, self.author_id, self.magazine_id)
            )
            self.id = cursor.fetchone()[0]
        else:  
            cursor.execute(
                """UPDATE articles SET title = ?, author_id = ?, magazine_id = ? 
                WHERE id = ?""",
                (self.title, self.author_id, self.magazine_id, self.id)
            )
        
        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        
        return cls(row['title'], row['author_id'], row['magazine_id'], row['id']) if row else None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        rows = cursor.fetchall()
        conn.close()
        
        return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                for row in rows]

    @classmethod
    def find_by_author(cls, author_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def author(self):
        from lib.models.author import Author  # Local import to break circular dependency
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (self.author_id,))
        row = cursor.fetchone()
        conn.close()
        return Author(row['name'], row['id']) if row else None

    def magazine(self):
        from lib.models.magazine import Magazine  # Local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (self.magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return Magazine(row['name'], row['category'], row['id']) if row else None