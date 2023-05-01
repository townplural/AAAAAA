import psycopg2


def create_db(conn):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS client_info(
            client_id SERIAL PRIMARY KEY,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            email TEXT UNIQUE
    );
        CREATE TABLE IF NOT EXISTS phone_numbers(
            client_id INTEGER REFERENCES client_info(client_id),
            phone_id SERIAL PRIMARY KEY,
            phone_number VARCHAR(40) UNIQUE
            );
    """)


def add_client(conn, first_name, last_name, email):
    cur.execute("""
        INSERT INTO client_info(first_name, last_name, email)
        VALUES  (%s, %s, %s);
    """, (first_name, last_name, email))

    print('Client has been added')

    # cur.execute("""
    # SELECT * FROM client_info;
    # """)
    # print(cur.fetchall())


def add_phone_number(conn, phone, client_id):
    cur.execute("""
        INSERT INTO phone_numbers(phone_number)
            VALUES(%s);
        UPDATE phone_numbers
            SET client_id = %s
            WHERE phone_number = %s;
    """, (phone, client_id, phone))
    print('Phone number has been added')

    # cur.execute("""
    # SELECT * FROM phone_numbers;
    # """)
    # print(cur.fetchall())


def edit_client_info(conn, client_id, param, param_value):

    cur.execute(f"""
        UPDATE client_info
        SET {param} = %s
        WHERE client_id = %s;
    """, (param_value, client_id))

    # cur.execute("""
    #     SELECT * FROM client_info;
    #     """)
    # print(cur.fetchall())


def delete_client_phone_number(conn, phone):
    cur.execute("""
        DELETE FROM phone_numbers
        WHERE phone_number = %s;
        """, (phone,))

    # cur.execute("""
    #      SELECT * FROM phone_numbers;
    #      """)
    # print(cur.fetchall())


def delete_client(conn, client_id):
    cur.execute("""
        DELETE FROM phone_numbers
        where client_id = %s;
        DELETE FROM client_info
        WHERE client_id = %s;
    """, (client_id,client_id))

    # cur.execute("""
    #      SELECT * FROM client_info;
    #      """)
    # print(cur.fetchall())
    print('Client has been deleted')


def find_client(conn, param, param_value):
    cur.execute(f"""
        SELECT * FROM client_info
        WHERE {param} = %s;
    """, (param_value,))
    print(cur.fetchone())


with psycopg2.connect(database='postgres-python', user='postgres', password='123322213') as conn:
    with conn.cursor() as cur:
        cur.execute("""
            DROP TABLE phone_numbers, client_info;
        """)

        create_db(conn=conn)
        add_client(conn, 'Ivan', 'Ivanov', 'ivanov.ivan@gmail.com')
        add_client(conn, 'Alex', 'Popovich', 'popovich.alex@gmail.com')
        add_phone_number(conn, '8(800)555-35-35', 1)
        add_phone_number(conn, '8(800)555-36-36', 1)
        add_phone_number(conn, '8(800)555-37-37', 2)
        edit_client_info(conn, 1, 'last_name', param_value='Tugarin')
        delete_client_phone_number(conn, "8(800)555-36-36")
        delete_client(conn, 1)
        find_client(conn, 'email', 'popovich.alex@gmail.com')


conn.close()
