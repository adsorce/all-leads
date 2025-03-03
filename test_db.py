import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Function to test the connection
def test_db_connection():
    try:
        # Connect to Supabase PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Run a test query
        cur.execute("SELECT 1;")
        result = cur.fetchone()

        # Check if query ran successfully
        if result and result[0] == 1:
            print("✅ Successfully connected to the Supabase database!")
        else:
            print("⚠ Database connection test failed.")

        # Close connection
        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Failed to connect to the database:", e)

# Run the test
if __name__ == "__main__":
    test_db_connection()
