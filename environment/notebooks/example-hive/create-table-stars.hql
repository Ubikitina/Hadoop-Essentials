CREATE TABLE stars(
     Name STRING,
     Constellation STRING,
     BayernDesignation STRING,
     Designation STRING,
     ApprovalDate DATE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/example-hive/'
TBLPROPERTIES ("skip.header.line.count"="1");
