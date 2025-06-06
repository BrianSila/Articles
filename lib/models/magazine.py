import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from db.connection import get_connection

class Magazine:
    def __init__(self, name, category, id=None):
        self.id = id 
        self._name = name
        self._category = category

    def __repr__(self):
        return f"Magazine(id={self.id}, name='{self.name}', category='{self.category}')"

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and 0 < len(value) <= 100:
            self._name = value
        else:
            raise ValueError("Name must be a string with length between 1 and 100")
        
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if isinstance(value, str) and 0 < len(value) <= 50:
            self._category = value
        else:
            raise ValueError("Category must be a string with length between 1 and 50")
        
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        if self.id is None:
            cursor.execute(
                "INSERT INTO magazines (name, category) VALUES (?, ?) RETURNING id",
                (self.name, self.category)
            )
            self.id = cursor.fetchone()[0]
        else:
            cursor.execute(
                "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                (self.name, self.category, self.id)
            )

        conn.commit()
        conn.close()
        return self

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        return cls(row['name'], row['category'], row['id']) if row else None
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()

        return cls(row['name'], row['category'], row['id']) if row else None
    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()

        return [cls(row['name'], row['category'], row['id']) for row in rows]

    def articles(self):
        from lib.models.article import Article  # Local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) 
                for row in rows]
    
    def contributors(self):
        from lib.models.author import Author  # Local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT authors.*
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [Author(row['name'], row['id']) for row in rows]

    def article_titles(self):
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        from lib.models.author import Author  # Local import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(articles.id) > 2
        """, (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [Author(row['name'], row['id']) for row in rows]
    
    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.*, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            ORDER BY article_count DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()

        return cls(row['name'], row['category'], row['id']) if row else None
    
    @classmethod
    def with_multiple_authors(cls):
        """Returns magazines that have articles from multiple authors"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.*
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
            HAVING COUNT(DISTINCT articles.author_id) > 1
        """)
        rows = cursor.fetchall()
        conn.close()
        return [cls(row['name'], row['category'], row['id']) for row in rows]
    
    @classmethod
    def article_counts(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT magazines.id, magazines.name, magazines.category, COUNT(articles.id) as article_count
            FROM magazines
            LEFT JOIN articles ON magazines.id = articles.magazine_id
            GROUP BY magazines.id
        """)
        results = cursor.fetchall()
        conn.close()
        return [
            {
                "id": row["id"],
                "name": row["name"],
                "category": row["category"],
                "article_count": row["article_count"]
            }
            for row in results
        ]