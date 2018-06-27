# Using pig to populate the Hbase database
# first is necessary create the table:
	# $ hbase shell
	# $ create 'users','userinfo' # create a new table called 'users' that consists of the following column families", and we're just giving it one column family named 'userinfo' in this case.
	# $ exit
# use less to see inside a pig file without run

users = LOAD '/user/maria_dev/ml-100k/u.user' 
USING PigStorage('|') 
AS (userID:int, age:int, gender:chararray, occupation:chararray, zip:int);

STORE users INTO 'hbase://users' # to store in table users
USING org.apache.pig.backend.hadoop.hbase.HBaseStorage (
'userinfo:age,userinfo:gender,userinfo:occupation,userinfo:zip');

# to take a look in the database
	# $ hbase shell
	# $ scan 'users'
# to remove the table
	# $ disable 'users'
	# $ drop 'users'
