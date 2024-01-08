import psycopg2

conn = psycopg2.connect(
    dbname='habblet',
    user='postgres',
    password='1234',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

create_users_table = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        figure VARCHAR(255)
    )
'''

create_badges_table = '''
    CREATE TABLE IF NOT EXISTS badges (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        badge_name VARCHAR(100)
    )
'''

create_groups_table = '''
    CREATE TABLE IF NOT EXISTS groups (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        group_name VARCHAR(255)
    )
'''

create_rooms_table = '''
    CREATE TABLE IF NOT EXISTS rooms (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        room_name VARCHAR(255)
    )
'''

create_friends_table = '''
    CREATE TABLE IF NOT EXISTS friends (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        friend_id INTEGER REFERENCES users(id)
    )
'''

try:
    cur.execute(create_users_table)
    cur.execute(create_badges_table)
    cur.execute(create_groups_table)
    cur.execute(create_rooms_table)
    cur.execute(create_friends_table)
    conn.commit()
    print("Tabelas criadas com sucesso.")
except psycopg2.Error as e:
    conn.rollback()
    print("Erro ao criar as tabelas:", e)

cur.close()
conn.close()
