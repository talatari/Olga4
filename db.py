#################################################
##                  v.1.0                      ##
#################################################
import sqlite3


def ensure_connection(func):
    def inner(*args, **kwargs):
        #with sqlite3.connect('DB/DATABASE.DB') as con:
        with sqlite3.connect('DB/PROM.DB') as con:
            res = func(*args, con=con, **kwargs)
        return res
    return inner

@ensure_connection
def init_db(con, FORCE_SAVES: bool = False, FORCE_CATALOGS: bool = False, FORCE_USERS: bool = False):
    cur = con.cursor()

    if FORCE_SAVES:
        cur.execute('DROP TABLE IF EXISTS SAVES')
        print('\n' + "Очищена таблица SAVES" + '\n')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS SAVES (
            ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            CATALOG_ID  INTEGER NOT NULL,
            URL         TEXT
        )
    ''')

    if FORCE_CATALOGS:
        cur.execute('DROP TABLE IF EXISTS CATALOGS')
        print('\n' + "Очищена таблица CATALOGS" + '\n')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS CATALOGS (
            ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            NAME        TEXT
        )
    ''')

    if FORCE_USERS:
        cur.execute('DROP TABLE IF EXISTS USERS')
        print('\n' + "Очищена таблица USERS" + '\n')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            ID          INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            USER_ID     INTEGER NOT NULL UNIQUE,
            FIRST_NAME  TEXT,
            LAST_NAME   TEXT,
            USER_NAME   TEXT,
            PERMISSIONS TEXT,
            PAGE        TEXT
        )
    ''')

    con.commit()

###################################################### INSERTS ########################################################

@ensure_connection
def ins_cat(con, NAME: str):
    cur = con.cursor()
    cur.execute('INSERT INTO CATALOGS (NAME) VALUES (?)', (NAME,))
    con.commit()

@ensure_connection
def ins_saves(con, CATALOG_ID: int, URL: str):
    cur = con.cursor()
    cur.execute('INSERT INTO SAVES (CATALOG_ID, URL) VALUES (?, ?)', (CATALOG_ID, URL))
    con.commit()

@ensure_connection
def ins_users(con, USER_ID: int, FIRST_NAME: str, LAST_NAME: str, USER_NAME: str, PERMISSIONS: str, PAGE: str):
    cur = con.cursor()
    cur.execute('INSERT INTO USERS (USER_ID, FIRST_NAME, LAST_NAME, USER_NAME, PERMISSIONS, PAGE) '
                'VALUES (?, ?, ?, ?, ?, ?)', (USER_ID, FIRST_NAME, LAST_NAME, USER_NAME, PERMISSIONS, PAGE))
    con.commit()

###################################################### UPDATES ########################################################

@ensure_connection
def add_perm(con, USER_ID: int):
    cur = con.cursor()
    cur.execute('UPDATE USERS SET PERMISSIONS = 1 WHERE USER_ID = ?', (USER_ID,))
    con.commit()

@ensure_connection
def kill_perm(con, USER_ID: int):
    cur = con.cursor()
    cur.execute('UPDATE USERS SET PERMISSIONS = 0 WHERE USER_ID = ?', (USER_ID,))
    con.commit()

@ensure_connection
def up_page_user(con, PAGE, USER_ID):
    cur = con.cursor()
    cur.execute("UPDATE USERS SET PAGE = ? WHERE USER_ID = ?", (PAGE, USER_ID,))
    con.commit()

@ensure_connection
def up_name_catalog(con, NAME, ID):
    cur = con.cursor()
    cur.execute("UPDATE CATALOGS SET NAME = ? WHERE ID = ?", (NAME, ID,))
    con.commit()

###################################################### SELECTS ########################################################

@ensure_connection
def get_count_catalogs(con):
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM CATALOGS")
    return cur.fetchone()

@ensure_connection
def get_catalogs(con):
    cur = con.cursor()
    cur.execute("SELECT NAME FROM CATALOGS")
    return cur.fetchall()

@ensure_connection
def check_catalog(con, NAME):
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM CATALOGS WHERE NAME = ?", (NAME,))
    return cur.fetchone()

@ensure_connection
def check_id_catalog(con, NAME):
    cur = con.cursor()
    cur.execute("SELECT ID FROM CATALOGS WHERE NAME = ?", (NAME,))
    return cur.fetchone()

@ensure_connection
def check_name_catalog(con, ID):
    cur = con.cursor()
    cur.execute("SELECT NAME FROM CATALOGS WHERE ID = ?", (ID,))
    return cur.fetchone()

@ensure_connection
def list_urls(con, CATALOG_ID: int):
    cur = con.cursor()
    cur.execute("SELECT URL FROM SAVES WHERE CATALOG_ID = ?", (CATALOG_ID,))
    return cur.fetchall()

@ensure_connection
def check_id_user(con, USER_ID):
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM USERS WHERE USER_ID = ?", (USER_ID,))
    return cur.fetchone()

@ensure_connection
def check_perm_user(con, USER_ID):
    cur = con.cursor()
    cur.execute("SELECT PERMISSIONS FROM USERS WHERE USER_ID = ?", (USER_ID,))
    return cur.fetchone()

@ensure_connection
def check_page_user(con, USER_ID):
    cur = con.cursor()
    cur.execute("SELECT PAGE FROM USERS WHERE USER_ID = ?", (USER_ID,))
    return cur.fetchone()

###################################################### DELETES ########################################################

@ensure_connection
def delete_saves(con, ID):
    cur = con.cursor()
    cur.execute("DELETE FROM SAVES WHERE CATALOG_ID = ?", (ID,))
    con.commit()

@ensure_connection
def delete_catalog(con, ID):
    cur = con.cursor()
    cur.execute("DELETE FROM CATALOGS WHERE ID = ?", (ID,))
    con.commit()

@ensure_connection
def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM USERS WHERE PERMISSIONS = 0")
    con.commit()

#######################################################################################################################

# try:
#     print(check_page_user(USER_ID=441039920))
#
# except sqlite3.Error as e:
#     print('\n' + "Произошла ошибка:" + '\n' + '\n', e.args[0])

#######################################################################################################################






































