# export SPARK_MAJOR_VERSION = 2, use this command in server because the following code is version 2 of Spark

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions

def parseInput(line):
    fields = line.split('|')
    return Row(user_id = int(fields[0]), age = int(fields[1]), gender = fields[2], occupation = fields[3], zip = fields[4])

if __name__ == "__main__":
    # Create a SparkSession
    spark = SparkSession.builder.appName("CassandraIntegration").config("spark.cassandra.connection.host", "127.0.0.1").getOrCreate() # in this case running on localhost "127.0.0.1"

    # Get the raw data
    lines = spark.sparkContext.textFile("hdfs:///user/eksz/ml-100k/u.data")
    # Convert it to a RDD of Row objects with (userID, age, gender, occupation, zip)
    users = lines.map(parseInput)
    # Convert that to a DataFrame
    usersDataset = spark.createDataFrame(users)

    # Write it into Cassandra
    usersDataset.write\
        .format("org.apache.spark.sql.cassandra")\ # Set connection with Cassandra
        .mode('append')\
        .options(table="users", keyspace="movielens")\  # it was created in Cassandra
        .save()

    # Read it back from Cassandra into a new Dataframe
    readUsers = spark.read\
    .format("org.apache.spark.sql.cassandra")\
    .options(table="users", keyspace="movielens")\
    .load() 

    readUsers.createOrReplaceTempView("users") 

    sqlDF = spark.sql("SELECT * FROM users WHERE age < 20")
    sqlDF.show()

    # Stop the session
    spark.stop()

    # Now, one little trick: you can't just pass in "org.apache.datastax.sql.cassandra" and expect it to just work - it has to know where to find that packet.
    # So we do need to pass that in as a parameter to our script, when we run it. So let's do it this way: 
    # in cluster shell: spark-submit --packages datastax:spark-cassandra-connector:2.0.0-M2-s 2.11 cassandraSpark.py
    # that's sort of a wrapper script for Spark that submits the script to our cluster, and we'll say,
    # "--packages datastax:spark-cassandra-connector:2.0.0-M2-s_2.11". Again, that specific package name might change in the future.
    # This is saying that I want the version of the connector that is compatible with Spark 2.0 and Scala version 2.11.