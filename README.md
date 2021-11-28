# Homework #9 for Highload:Projector

DB Isolation & Locks


## Installation

```
git clone https://github.com/god-of-north/highload-homework-9.git
cd highload-homework-9
docker-compose run
pip install -r requirements.txt
```


## Percona test results

### Non-repeatable reads: 

#### READ UNCOMMITTED:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
    START TRANSACTION; 
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', 'death star', 50)
    UPDATE users SET password = '3333333' WHERE id = 1;
    COMMIT; 
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', '3333333', 50)
COMMIT;
```


#### READ COMMITTED:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
    SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
    START TRANSACTION;
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', 'death star', 50)
    UPDATE users SET password = '3333333' WHERE id = 1;
    COMMIT; 
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', '3333333', 50)
COMMIT;
```


#### REPEATABLE READ

```
SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
    START TRANSACTION;
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', 'death star', 50)
    UPDATE users SET password = '3333333' WHERE id = 1;
    COMMIT;
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', '3333333', 50)
COMMIT;
```


#### SERIALIZABLE

```
SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
    START TRANSACTION;
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', 'death star', 50)
    UPDATE users SET password = '3333333' WHERE id = 1;
    COMMIT;
SELECT * FROM users WHERE id = 1;
(1, 'Darth Vader', 'death star', 50)
COMMIT;
```


### Phantom reads:

#### READ UNCOMMITTED:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
    START TRANSACTION;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
    INSERT INTO users(username, password) VALUES ('Masgister Yoda', 'murmurmur');
    COMMIT;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
(5, 'Masgister Yoda', 'murmurmur', None)
COMMIT;
```


#### READ COMMITTED:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
    SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
    START TRANSACTION;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
    INSERT INTO users(username, password) VALUES ('Masgister Yoda', 'murmurmur');
    COMMIT;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
(5, 'Masgister Yoda', 'murmurmur', None)
COMMIT;
```


#### REPEATABLE READ:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
    INSERT INTO users(username, password) VALUES ('Masgister Yoda', 'murmurmur');
    COMMIT;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
(5, 'Masgister Yoda', 'murmurmur', None)
COMMIT;
```


#### SERIALIZABLE:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
    START TRANSACTION;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
    INSERT INTO users(username, password) VALUES ('Masgister Yoda', 'murmurmur');
    COMMIT;
SELECT * FROM users WHERE id>2;
(3, 'Chewbakka', 'rrraarGhhrraarr', 123)
(4, 'R2D2', 'peep-peeep', 444)
COMMIT;
```


### Dirty reads:


#### READ UNCOMMITTED:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
    SET GLOBAL TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
START TRANSACTION;
    START TRANSACTION;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'death star', 50)
UPDATE users SET password = 'qwerty' WHERE id = 1;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'qwerty', 50)
ROLLBACK;
    COMMIT;
```


#### READ COMMITTED:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
    SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;
START TRANSACTION;
    START TRANSACTION; 
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'death star', 50)
UPDATE users SET password = 'qwerty' WHERE id = 1;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'qwerty', 50)
ROLLBACK;
    COMMIT;
```


#### REPEATABLE READ:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
    SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
START TRANSACTION;
    START TRANSACTION;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'death star', 50)
UPDATE users SET password = 'qwerty' WHERE id = 1;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'death star', 50)
ROLLBACK;
    COMMIT;
```


#### SERIALIZABLE:

```
SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    SET GLOBAL TRANSACTION ISOLATION LEVEL SERIALIZABLE;
START TRANSACTION;
    START TRANSACTION;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'death star', 50)
UPDATE users SET password = 'qwerty' WHERE id = 1;
    SELECT * FROM users WHERE id = 1;
    (1, 'Darth Vader', 'death star', 50)
ROLLBACK;
    COMMIT;
```
	
