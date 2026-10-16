import psycopg2
from db_config import POSTGRES_CONFIG, DATABASES


def connect_to_database(database_name):
    """Create and return a connection to a PostgreSQL database."""

    return psycopg2.connect(
        dbname=database_name,
        **POSTGRES_CONFIG
    )


def display_rows(connection, table):
    """Display all rows from the selected table."""

    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table} ORDER BY id;")
    rows = cursor.fetchall()

    print("\n----------------------------------------")

    if not rows:
        print("No data found.")
    else:
        for row in rows:
            print(row)

    print("----------------------------------------")

    cursor.close()


def insert_student(connection):
    name = input("Student name: ")
    email = input("Email: ")
    study_year = int(input("Study year: "))

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students (name, email, study_year)
        VALUES (%s, %s, %s);
    """, (name, email, study_year))

    connection.commit()
    cursor.close()

    print("Student added successfully.")


def insert_product(connection):
    name = input("Product name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products (name, price, stock)
        VALUES (%s, %s, %s);
    """, (name, price, stock))

    connection.commit()
    cursor.close()

    print("Product added successfully.")


def insert_book(connection):
    title = input("Book title: ")
    author = input("Author: ")
    publication_year = int(input("Publication year: "))

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, publication_year)
        VALUES (%s, %s, %s);
    """, (title, author, publication_year))

    connection.commit()
    cursor.close()

    print("Book added successfully.")


def insert_row(connection, table):
    """Insert data depending on the selected database."""

    if table == "students":
        insert_student(connection)

    elif table == "products":
        insert_product(connection)

    elif table == "books":
        insert_book(connection)


def update_row(connection, table):
    """Update a row selected by its ID."""

    display_rows(connection, table)

    row_id = int(input("\nEnter the ID to update: "))

    cursor = connection.cursor()

    if table == "students":
        name = input("New name: ")
        email = input("New email: ")
        study_year = int(input("New study year: "))

        cursor.execute("""
            UPDATE students
            SET name = %s,
                email = %s,
                study_year = %s
            WHERE id = %s;
        """, (name, email, study_year, row_id))

    elif table == "products":
        name = input("New product name: ")
        price = float(input("New price: "))
        stock = int(input("New stock: "))

        cursor.execute("""
            UPDATE products
            SET name = %s,
                price = %s,
                stock = %s
            WHERE id = %s;
        """, (name, price, stock, row_id))

    elif table == "books":
        title = input("New title: ")
        author = input("New author: ")
        publication_year = int(input("New publication year: "))

        cursor.execute("""
            UPDATE books
            SET title = %s,
                author = %s,
                publication_year = %s
            WHERE id = %s;
        """, (title, author, publication_year, row_id))

    connection.commit()

    if cursor.rowcount == 0:
        print("No row with that ID was found.")
    else:
        print("Row updated successfully.")

    cursor.close()


def delete_row(connection, table):
    """Delete a row by ID."""

    display_rows(connection, table)

    row_id = int(input("\nEnter the ID to delete: "))

    cursor = connection.cursor()

    cursor.execute(
        f"DELETE FROM {table} WHERE id = %s;",
        (row_id,)
    )

    connection.commit()

    if cursor.rowcount == 0:
        print("No row with that ID was found.")
    else:
        print("Row deleted successfully.")

    cursor.close()


def database_menu(database_name, table):
    """Menu displayed after the user selects a database."""

    try:
        connection = connect_to_database(database_name)

    except psycopg2.Error as error:
        print(f"Could not connect to database: {error}")
        return

    while True:
        print(f"\n=== Connected to {database_name} ===")
        print("1. Read data")
        print("2. Add data")
        print("3. Update data")
        print("4. Delete data")
        print("5. Return to database selection")

        choice = input("\nSelect an option: ")

        try:
            if choice == "1":
                display_rows(connection, table)

            elif choice == "2":
                insert_row(connection, table)

            elif choice == "3":
                update_row(connection, table)

            elif choice == "4":
                delete_row(connection, table)

            elif choice == "5":
                break

            else:
                print("Invalid option.")

        except ValueError:
            print("Invalid value. Please enter the correct data type.")

        except psycopg2.Error as error:
            connection.rollback()
            print(f"Database error: {error}")

    connection.close()


def main():
    while True:
        print("\n================================")
        print(" PostgreSQL Database Application")
        print("================================")
        print("1. University database")
        print("2. Shop database")
        print("3. Library database")
        print("4. Exit")

        choice = input("\nSelect a database: ")

        if choice in DATABASES:
            database = DATABASES[choice]

            database_menu(
                database["name"],
                database["table"]
            )

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid selection.")


if __name__ == "__main__":
    main()