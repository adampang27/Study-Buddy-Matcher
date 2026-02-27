import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Database Configuration ---

# Get database connection parameters from environment variables with defaults for local dev
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "smart_buddy")

# Prioritize DATABASE_URL if it exists 
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # SQLAlchemy requires "postgresql://"
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Construct MySQL URL from individual components
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Detect if the application is running on a platform like Render
is_render = "RENDER" in os.environ

# --- SQLAlchemy Engine Setup ---

try:
    # Create the SQLAlchemy engine using the determined URL
    engine = create_engine(DATABASE_URL)

    # Create a configured "Session" class
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create a Base class for declarative models
    Base = declarative_base()

    # Test the database connection to ensure it's working
    with engine.connect() as connection:
        print("Database connection established successfully!")

except Exception as e:
    print(f"ERROR: Database connection failed: {e}", file=sys.stderr)
    if is_render:
        print("Hint: Ensure the DATABASE_URL environment variable is correctly set in your deployment environment.", file=sys.stderr)
    else:
        print("Hint: Check that your local MySQL server is running, PyMySQL is installed (`pip install pymysql`), and the .env file has the correct credentials.", file=sys.stderr)
    raise

# --- Database Session Dependency ---

def get_db():
    """
    Dependency function to get a database session for each request.
    Ensures the session is always closed after the request.
    """
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
def create_tables():
    """Create all database tables defined by models inheriting from Base."""
    try:
        # Import models to ensure they're registered with the Base
        from smart_buddy.sqlalchemy_models import Profile, Session, Rating
        Base.metadata.create_all(bind=engine)
        print("Database tables checked/created successfully.")
    except Exception as e:
        print(f"ERROR: Failed to create database tables: {e}", file=sys.stderr)
        raise

# Initialize the database by creating tables
create_tables()
