import psycopg2
from psycopg2 import sql
from db_config import POSTGRES_CONFIG


DATABASE_NAMES = [
    "university_db",
    "shop_db",
    "library_db"
]


def create_databases():
    """
    Connect to the default postgres database and create
    the three databases if they do not already exist.
    """

    connection = psycopg2.connect(
        dbname="postgres",
        **POSTGRES_CONFIG
    )

    
    connection.autocommit = True

    cursor = connection.cursor()

    for database_name in DATABASE_NAMES:

        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database_name,)
        )

        exists = cursor.fetchone()

        if not exists:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
            )

            print(f"Created database: {database_name}")
        else:
            print(f"Database already exists: {database_name}")

    cursor.close()
    connection.close()


def setup_university_database():
    connection = psycopg2.connect(
        dbname="university_db",
        **POSTGRES_CONFIG
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            study_year INTEGER NOT NULL
        );
    """)

   
    cursor.execute("TRUNCATE TABLE students RESTART IDENTITY;")

    students = [
        ("Alice Johnson", "alice@example.com", 1),
        ("Bob Smith", "bob@example.com", 2),
        ("Charlie Brown", "charlie@example.com", 3),
        ("Diana Miller", "diana@example.com", 4)
    ]

    cursor.executemany("""
        INSERT INTO students (name, email, study_year)
        VALUES (%s, %s, %s);
    """, students)

    connection.commit()
    cursor.close()
    connection.close()

    print("University database initialized.")


def setup_shop_database():
    connection = psycopg2.connect(
        dbname="shop_db",
        **POSTGRES_CONFIG
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            stock INTEGER NOT NULL
        );
    """)

    cursor.execute("TRUNCATE TABLE products RESTART IDENTITY;")

    products = [
        ("Laptop", 999.99, 10),
        ("Keyboard", 49.90, 25),
        ("Mouse", 24.50, 50),
        ("Monitor", 249.00, 15)
    ]

    cursor.executemany("""
        INSERT INTO products (name, price, stock)
        VALUES (%s, %s, %s);
    """, products)

    connection.commit()
    cursor.close()
    connection.close()

    print("Shop database initialized.")


def setup_library_database():
    connection = psycopg2.connect(
        dbname="library_db",
        **POSTGRES_CONFIG
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            author VARCHAR(100) NOT NULL,
            publication_year INTEGER NOT NULL
        );
    """)

    cursor.execute("TRUNCATE TABLE books RESTART IDENTITY;")

    books = [
        ("1984", "George Orwell", 1949),
        ("The Hobbit", "J.R.R. Tolkien", 1937),
        ("Dune", "Frank Herbert", 1965),
        ("The Pragmatic Programmer", "Andrew Hunt", 1999)
    ]

    cursor.executemany("""
        INSERT INTO books (title, author, publication_year)
        VALUES (%s, %s, %s);
    """, books)

    connection.commit()
    cursor.close()
    connection.close()

    print("Library database initialized.")


def main():
    print("Setting up PostgreSQL databases...\n")

    create_databases()

    setup_university_database()
    setup_shop_database()
    setup_library_database()

    print("\nSetup completed successfully.")


if __name__ == "__main__":
    main()