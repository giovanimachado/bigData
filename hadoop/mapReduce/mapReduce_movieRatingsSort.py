from mrjob.job import MRJob
from mrjob.step import MRStep

class RatingBreakdown(MRJob): #This parenthesis MR job just means that ratings_breakdown inherits from the MR job class as part of the job package.
	def steps(self):
		return [
			MRStep(mapper=self.mapper_get_pop,
				reducer=self.reducer_count_ratings),#it tells the framework what functions are used for mappers and reducers in our jobs.
			MRStep(reducer=self.reducer_sorter)

		]

	def mapper_get_pop(self, _, line):
		(userID, movieID, rating, timestamp) = line.split('\t')
		yield movieID, 1

	def reducer_count_ratings(self, key, values):
		yield str(sum(values)).zfill(5), key #streaming consider values as string / Necessary fill with 0

	def reducer_sorter(self, count, movies):
		for movie in movies:
			yield movie, count


if __name__=='__main__': # if we're executing this script from a command-line go ahead and kick this job off.
	RatingBreakdown.run()

#Run locally: 
#	python mapReduce_movieRatings.py u.data

#Run with Hadoop: 
#	python mapReduce_movieRatings.py -r hadoop --hadoop-streaming-jar
#	/usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data 
#In this case the u.data in local
#	python mapReduce_movieRatings.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar u.data 
# For run in hdfs
#	python mapReduce_movieRatings.py -r hadoop --hadoop-streaming-jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar hdfs://FOLDER/u.data 