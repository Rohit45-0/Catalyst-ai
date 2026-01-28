from sqlalchemy import text
from app.db.session import get_engine
import os
from dotenv import load_dotenv

load_dotenv()

def fix_db_schema():
    engine = get_engine()
    print("Checking database schema for missing columns...")
    
    with engine.connect() as conn:
        # Check if columns exist in projects table
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='projects';
        """))
        existing_columns = [row[0] for row in result]
        
        columns_to_add = {
            "campaign_goal": "TEXT",
            "target_audience": "TEXT",
            "brand_persona": "TEXT"
        }
        
        for col, col_type in columns_to_add.items():
            if col not in existing_columns:
                print(f"Adding missing column: {col}...")
                conn.execute(text(f"ALTER TABLE projects ADD COLUMN {col} {col_type};"))
                conn.commit()
                print(f"Successfully added {col}")
            else:
                print(f"Column {col} already exists.")
    
    print("Database schema is now up to date!")

if __name__ == "__main__":
    fix_db_schema()
