from db.connection import get_connection
from lib.models import Article, Author

class Magazine:

    def __init__(self, name, category, id=None):
        self.id = id 
        self._name = name
        self._category = category

    def __repr__(self):
        return f"Magazine(id={self.id}, 'name={self.name}, category={self.category}')"

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and 0 <len(value) <= 100:
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

        if row is None:
            return None
        return cls(row['name'], row['category'], row['id'])
    
    @classmethod
    def find_by_name(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()

        if row is None:
            return None
        return cls(row['name'], row['category'], row['id'])
    
    @classmethod
    def find_by_category(cls, category):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        row = cursor.fetchone()

        if row is None:
            return None
        return cls(row['name'], row['category'], row['id'])

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()

        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]
    
    def contributors(self):
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
        return [article._title for article in self.articles()]

    def contributing_authors(self):
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

        if row is None:
            return None
        return cls(row['name'], row['category'], row['id'])
    
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