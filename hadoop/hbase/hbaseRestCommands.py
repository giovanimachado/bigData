#Hbase commands for create a table for movie ratings by user
#It is necessary set the Hbase REST for port 8000 in the server (or virtual machine)
#In server shell (to launch a REST server sitting on top of Hbase): 
	# su root
	# /usr/hdp/current/hbase-master/bin/hbase-daemon.sh start rest -p 8000 --infoport 8001
# In this point the backend is running

from  starbase import Connection

c = Connection("127.0.0.1", "8000") # Connect to the port that REST server operates on

ratings = c.table('ratings') # create table ratings

if (ratings.exists()):
	print("Dropping existing ratings table")
	ratings.drop()

ratings.create('rating') # create a column family on table ratings

print("Parsig the ml-100k ratings data...\n")
ratingFile = open("e:/Downloads/ml-100k/ml-100k/u.data", "r") # necessary to adjust the path

batch = ratings.batch() #create a batch object from "ratings" table / starbase package has a batch interface,

for line in ratingFile:
	(userID, movieID, rating, timestamp = line.split()
	batch.update(userID, {'rating': {movieID : rating}}) # update the batch with the new rows, where the row ID is given by the user ID I extract from the "u.data" file, and I will say the "rating" 
														# column family is going to populate itself with a "rating" column
														 # of the movie ID with a given rating value. So this ends up with a row that has a unique key of the user ID. Under the "rating" column family, 
														 # we can construct individual columns for each unique movie ID, so the column will be given by
														 # "Rating:<movie ID>", and the actual value in each cell is the rating itself.

ratingFile.close() # close the rating files because it was read

print("Committing ratings data to Hbase via REST service\n")
batch.commit(finalize=TRUE) # commit the batch through the service, so it actually gets written into HBase

print("Get back ratings for some users...\n")
print("Ratings for user ID 1:\n")
print(ratings.fetch("1"))
print("Ratings for user ID 33:\n")
print(ratings.fetch("33"))

#Hbase has a tool called "importtsv"