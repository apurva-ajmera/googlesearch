#create a class to store data for forward indexing
class Forward_Index():
	#declare dictionary for saving data of webpages with it's url
	forward_indexing_dict = {'data':{}}

	def for_indexing(self, name, list_of_words):
		self.forward_indexing_dict['data'][name] = []

		for words in list_of_words:
			if name in self.forward_indexing_dict['data'].keys():
				self.forward_indexing_dict['data'][name].append(words)
			else:
				self.forward_indexing_dict['data'][name] = []
				self.forward_indexing_dict['data'][name].append(words)
