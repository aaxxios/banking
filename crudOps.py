from pathlib import Path
import sqlite3


BASE = Path(__file__).parent
DB = BASE/'bank.sqlite3'


def execute(conn, query, params=None, output=True):
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    res = cur.fetchall()
    conn.commit()
    conn.close()
    if output:
        return res


def setup_db():
    conn = sqlite3.connect(DB)
    query = '''
        CREATE TABLE IF NOT EXISTS banking(
            number TEXT PRIMARY KEY,
            pin TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            balance INTEGER DEFAULT 0,
            hibernated INTEGER DEFAULT 0
        )
    '''
    execute(conn, query, output=False)


def get_connection():
    return sqlite3.connect(DB)


def add_user(number, name, phone, pin):
    conn = sqlite3.connect(DB)

    query = '''

        INSERT INTO banking( number, name, phone, pin)
                    VALUES ( ?,?,?, ?)
    '''
    execute(conn, query, [number, name, phone, pin], False)
   

def get_numbers():
    conn = sqlite3.connect(DB)
    query = '''
    SELECT number from banking'''
    return execute(conn, query)


def hibernate_user(number, sec):
    conn = sqlite3.connect(DB)
    query = '''
    UPDATE banking SET hibernated = ?
    WHERE number = {}
    '''.format(number)
    execute(conn, query, [sec], False)


def update_balance(number, amount, key=1):
    conn = sqlite3.connect(DB)
    query = '''
    UPDATE banking set balance = balance - ?
    WHERE number = {}
    '''.format(number)
    query2 = '''
    UPDATE banking set balance = balance + ?
    WHERE number = {}
    '''.format(number)
    if key == 1:
        execute(conn, query, [amount], False)
    else:
        execute(conn, query2, [amount], False)


def get_users():
    conn = sqlite3.connect(DB)
    query = '''

        SELECT number, name, phone
        FROM banking
    '''
    return execute(conn, query)


def get_user_by_number(number):
    conn = sqlite3.connect(DB)

    query = '''

        SELECT number, name, pin, balance, hibernated
        FROM banking
        WHERE number = {}
    ''' .format(number)
    return execute(conn, query)


def transfer(sender, recipient, amount):
    conn = sqlite3.connect(DB)
    query = '''
    BEGIN;
    UPDATE banking SET balance = balance - {amount}
    WHERE number = {sender};
    UPDATE banking SET balance = balance + {amount}
    WHERE number = {rec};
    COMMIT
    '''
    cur = conn.cursor()
    cur.execute(query)


def update_user_details(number, name, phone):
    conn = sqlite3.connect(DB)

    query = '''
        UPDATE banking
        SET name = ?, phone = ?
        WHERE number = ?
    '''
    execute(conn, query, params=[number, name, phone], output=False)


def delete_banking(number):
    conn = sqlite3.connect(DB)

    query = '''

        DELETE
        FROM banking
        WHERE number = {}
    with conn.cursor() as cur:
    ''' .format(number)
    execute(conn, query, output=False)
