import psycopg2
from config import load_config

def connect():
    connection = None
    try:
        params = load_config()
        print("Connecting to PostgreSQL...")
        connection = psycopg2.connect(**params)

        cursor = connection.cursor()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terrminated")

def insert_species(species_name):
    """
        Insert new species into species table
    """
    sql = """INSERT INTO species(species_name)
             VALUES(%s) RETURNING species_id;"""
    
    species_id = None
    config = load_config()
    rows = []
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (species_name, ))
                rows = cur.fetchone()
                if rows:
                    species_id = rows[0]
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return rows                

def insert_species_images():
    """
    
    """
    return

def insert_species_annotations():
    """
    
    """
    return

if __name__ == "__main__":
    connect()