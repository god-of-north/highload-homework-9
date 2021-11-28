import time
import timeout_decorator
import mysql.connector


def create_table():
    with mysql.connector.connect(host="localhost", user="root", password="root", database="db") as conn:
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION;')
            cursor.execute('DROP TABLE IF EXISTS users;')
            cursor.execute('CREATE TABLE users (id int NOT NULL AUTO_INCREMENT, username VARCHAR(100),  password VARCHAR(100), age INT, PRIMARY KEY (id)) ENGINE=InnoDB;')
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('Darth Vader', 'death star', 50);")
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('Luke Skywalker', 'sdfdfsdf', 25);")
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('Chewbakka', 'rrraarGhhrraarr', 123);")
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('R2D2', 'peep-peeep', 444);")
        conn.commit()

def test(query:str, level:str):
    query = query.replace("[LEVEL]", level)
    query = [line for line in query.split("\n") if line.strip() != ""]

    conn1 = mysql.connector.connect(host="localhost", user="root", password="root", database="db")
    conn2 = mysql.connector.connect(host="localhost", user="root", password="root", database="db")
    c1 = conn1.cursor()
    c2 = conn2.cursor()

    for line in query:
        if line.startswith(' '):
            if line.strip().startswith('[FETCH]'):
                result = c2.fetchall()
                for row in result:
                    print('   ', row)
            else:
                print(line)
                c2.execute(line[1:])
        else:
            if line.strip().startswith('[FETCH]'):
                result = c1.fetchall()
                for row in result:
                    print(row)
            else:
                print(line)
                c1.execute(line)

    c1.close()
    c2.close()
    conn1.close()
    conn2.close()

def test_with_levels(query):
    print('\r\n')
    create_table()
    print('READ UNCOMMITTED:')
    test(query, 'READ UNCOMMITTED')

    print('\r\n')
    create_table()
    print('READ COMMITTED:')
    test(query, 'READ COMMITTED')

    print('\r\n')
    create_table()
    print('REPEATABLE READ:')
    test(query, 'REPEATABLE READ')

    print('\r\n')
    create_table()
    print('SERIALIZABLE:')
    test(query, 'SERIALIZABLE')


dirty_reads_query = """
SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
    SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
START TRANSACTION;
    START TRANSACTION; 

    SELECT * FROM users WHERE id = 1;
    [FETCH]
UPDATE users SET password = 'qwerty' WHERE id = 1;
    SELECT * FROM users WHERE id = 1;
    [FETCH]

ROLLBACK;
    COMMIT;
"""

non_repeatable_reads_query = """
SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
    SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
START TRANSACTION;
    START TRANSACTION; 
SELECT * FROM users WHERE id = 1;
[FETCH]
    UPDATE users SET password = '3333333' WHERE id = 1;
    COMMIT; 
SELECT * FROM users WHERE id = 1;
[FETCH]
COMMIT;
"""

phantom_reads_query = """
SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
    SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
START TRANSACTION;
    START TRANSACTION; 

SELECT * FROM users WHERE id>2;
[FETCH]
    INSERT INTO users(username, password) VALUES ('Masgister Yoda', 'murmurmur');
    COMMIT;
SELECT * FROM users WHERE id>2;
[FETCH]
COMMIT;
"""

lost_update_query = """
SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
    SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
START TRANSACTION;
    START TRANSACTION; 

UPDATE users SET age = age+10 WHERE id = 2;

    UPDATE users SET age = age+5 WHERE id = 2;
    COMMIT;
SELECT * FROM users WHERE id=2;
[FETCH]
COMMIT;
"""

blocking_query = """
SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
    SET GLOBAL TRANSACTION ISOLATION LEVEL [LEVEL];
START TRANSACTION;
    START TRANSACTION; 

SELECT * FROM users WHERE id=2;
[FETCH]

UPDATE users SET password = '111111111' WHERE id = 2;

SELECT * FROM users WHERE id=2;
[FETCH]

    SELECT * FROM users WHERE id=2;
    [FETCH]
    UPDATE users SET password = '22222222222' WHERE id = 2;
    SELECT * FROM users WHERE id=2;
    [FETCH]
    COMMIT;

COMMIT;
SELECT * FROM users WHERE id=2;
[FETCH]
"""

print("Non-repeatable reads:")
test_with_levels(non_repeatable_reads_query)
print("Phantom reads:")
test_with_levels(phantom_reads_query)
print("Dirty reads:")
test_with_levels(dirty_reads_query)
#print("Lost update:")
#test_with_levels(lost_update_query )


