-- This is meant to be run in Postgresql, like this:
-- psql <db-name> -f day11.sql
-- or
-- psql <db-name> < day11.sql
-- To change which file is processed, do so below, in the \COPY line.
--
-- SQL was a poor choice for this and the part 2 ran for almost 5 hours.
-- There is a nice linear algebra interpretation, so I might redo this in
-- some other language in the future.

\t
\o /dev/null

DROP TABLE IF EXISTS aoc201811_input;
DROP FUNCTION IF EXISTS aoc201811_f(int, int, int);
DROP FUNCTION IF EXISTS aoc201811_f(int, int, int, int);

CREATE TEMPORARY TABLE aoc201811_input (fieldsize int, value int);

\COPY aoc201811_input (fieldsize, value) FROM 'day11.in' WITH (FORMAT CSV);
SELECT * FROM aoc201811_input;

CREATE FUNCTION aoc201811_f(int, int, int, int) RETURNS bigint AS
    $$
    -- serial number, x, y, size
    SELECT SUM((((x + 10) * y + $1) * (x + 10) / 100) % 10 - 5)
        FROM generate_series($2, $2+$4-1) x, generate_series($3, $3+$4-1) y;
    $$
    LANGUAGE SQL;

CREATE FUNCTION aoc201811_f(int, int, int) RETURNS bigint AS 'select aoc201811_f($1, $2, $3, 3)' LANGUAGE SQL;

\o

WITH powers(x, y, power) AS (
    SELECT x, y, aoc201811_f(aoc201811_input.value, x, y)
    FROM
        aoc201811_input,
        generate_series(1, aoc201811_input.fieldsize - 2) x,
        generate_series(1, aoc201811_input.fieldsize - 2) y
),
maxpower (power) AS (
    SELECT MAX(power) FROM powers
)
SELECT 'Part 1: ' || x || ',' || y
FROM powers
WHERE power = (SELECT power FROM maxpower)
LIMIT 1;

WITH powers(x, y, size, power) AS (
    SELECT x, y, size, aoc201811_f(aoc201811_input.value, x, y, size)
    FROM
        aoc201811_input,
        generate_series(1, aoc201811_input.fieldsize) size,
        generate_series(1, aoc201811_input.fieldsize - size + 1) x,
        generate_series(1, aoc201811_input.fieldsize - size + 1) y
),
maxpower (power) AS (
    SELECT MAX(power) FROM powers
)
SELECT DISTINCT ON (power) 'Part 2: ' || x || ',' || y || ',' || size
FROM powers
WHERE power >= ALL(SELECT power FROM maxpower)
LIMIT 1;

\o /dev/null

DROP TABLE aoc201811_input;
DROP FUNCTION aoc201811_f(int, int, int);
DROP FUNCTION aoc201811_f(int, int, int, int);
