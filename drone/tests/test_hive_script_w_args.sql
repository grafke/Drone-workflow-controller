show tables;

DROP TABLE IF EXISTS test_table;
CREATE EXTERNAL TABLE test_table
(
columna INT,
columnb INT,
columnc INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION 's3://${BASE_DATA}/tmp/test_table/';
SELECT * FROM test_table;


DROP TABLE IF EXISTS test_table_out;

 CREATE EXTERNAL TABLE test_table_out
    (
    columna INT,
    columnb INT,
    columnc INT
    )
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
LINES TERMINATED BY '\n'
 STORED AS TEXTFILE
 LOCATION 's3://${BASE_DATA}/tmp/test_table_out/';

show tables;

SELECT * from test_table;

INSERT OVERWRITE TABLE
    test_table_out
SELECT
    columna,
    columnb,
    columnb
FROM
    test_table;

SELECT * FROM test_table_out;