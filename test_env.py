from dotenv import load_dotenv
import os

load_dotenv()

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
