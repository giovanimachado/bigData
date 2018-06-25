from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingBreakdown(MRJob): #This parenthesis MR job just means that ratings_breakdown inherits from the MR job class as part of the job package.
	def steps(self):
		return [
			MRStep(mapper=self.mapper_get_ratings,
				reducer=self.reducer_count_ratings)#it tells the framework what functions are used for mappers and reducers in our jobs.

		]

	def mapper_get_ratings(self, _, line):
		(userID, movieID, rating, timestamp) = line.split('\t')
		yield rating, 1

	def reducer_count_ratings(self, key, values):
		yield key, sum(values)

if __name__=='__main__': # if we're executing this script from a command-line go ahead and kick this job off.
	RatingBreakdown.run()

#
#Run locally: 
#	python mapReduce_movieRatings.py u.data

#Run with Hadoop: 
#	python mapReduce_movieRatings.py -r hadoop --hadoop-streaming-jar
#	/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data 
#In this case the u.data in local
#	python mapReduce_movieRatings.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data 
# For run in hdfs
#	python mapReduce_movieRatings.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs://FOLDER/u.data 