from lib.models import Author, Article, Magazine
from lib.db.connection import get_connection
from lib.db.seed import seed_database

class DebugConsole:
    def __init__(self):
        self.conn = get_connection()
        self.seed_sample_data()

    def seed_sample_data(self):
        """Add sample data if tables are empty"""
        if not Author.find_by_id(1):
            seed_database()
            print("✅ Sample data loaded")

    def start(self):
        print("\n🚀 Debug Console Ready")
        print("Available objects:")
        print("- conn: Database connection")
        print("- Author, Article, Magazine classes")
        print("- seed_database() to reset data")
        try:
            from IPython import embed
            embed(banner1="", colors="neutral")
        except ImportError:
            import code
            code.interact(local={**globals(), **locals()})

if __name__ == "__main__":
    DebugConsole().start()
