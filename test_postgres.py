import psycopg2

def create_table():
    with psycopg2.connect(dbname='postgres', user='pguser', password='secret', host='localhost', port=5432) as conn:
        with conn.cursor() as cursor:
            cursor.execute('DROP TABLE IF EXISTS users;')
            cursor.execute('CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(100),  password VARCHAR(100), age INT);')
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('Darth Vader', 'death star', 50);")
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('Luke Skywalker', 'sdfdfsdf', 25);")
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('Chewbakka', 'rrraarGhhrraarr', 123);")
            cursor.execute("INSERT INTO users (username, password, age) VALUES ('R2D2', 'peep-peeep', 444);")


def test(query:str, level:str):
    query = query.replace("[LEVEL]", level)
    query = [line for line in query.split("\n") if line.strip() != ""]

    conn1 = psycopg2.connect(dbname='postgres', user='pguser', password='secret', host='localhost', port=5432)
    conn2 = psycopg2.connect(dbname='postgres', user='pguser', password='secret', host='localhost', port=5432)
    c1 = conn1.cursor()
    c2 = conn2.cursor()

    for line in query:
        if line.startswith(' '):
            if line.strip().startswith('[FETCH]'):
                for row in c2:
                    print('   ', row)
            else:
                print(line)
                c2.execute(line[1:])
        else:
            if line.strip().startswith('[FETCH]'):
                for row in c1:
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
BEGIN TRANSACTION ISOLATION LEVEL [LEVEL];
    BEGIN TRANSACTION ISOLATION LEVEL [LEVEL]; 

    SELECT * FROM users WHERE id = 1;
    [FETCH]
UPDATE users SET password = 'qwerty' WHERE id = 1;
    SELECT * FROM users WHERE id = 1;
    [FETCH]

ROLLBACK;
    COMMIT;
"""

non_repeatable_reads_query = """
BEGIN TRANSACTION ISOLATION LEVEL [LEVEL];
    BEGIN TRANSACTION ISOLATION LEVEL [LEVEL]; 
SELECT * FROM users WHERE id = 1;
[FETCH]
    UPDATE users SET password = '3333333' WHERE id = 1;
    COMMIT; 
SELECT * FROM users WHERE id = 1;
[FETCH]
COMMIT;
"""

phantom_reads_query = """
BEGIN TRANSACTION ISOLATION LEVEL [LEVEL];
    BEGIN TRANSACTION ISOLATION LEVEL [LEVEL]; 

SELECT * FROM users WHERE id>2;
[FETCH]
    INSERT INTO users(username, password) VALUES ('Masgister Yoda', 'murmurmur');
    COMMIT;
SELECT * FROM users WHERE id>2;
[FETCH]
COMMIT;
"""

lost_update_query = """
BEGIN TRANSACTION ISOLATION LEVEL [LEVEL];
    BEGIN TRANSACTION ISOLATION LEVEL [LEVEL]; 

UPDATE users SET age = age+10 WHERE id = 2;

    UPDATE users SET age = age+5 WHERE id = 2;
    COMMIT;
SELECT * FROM users WHERE id=2;
[FETCH]
COMMIT;
"""

blocking_query = """
BEGIN TRANSACTION ISOLATION LEVEL [LEVEL];
    BEGIN TRANSACTION ISOLATION LEVEL [LEVEL]; 

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


