#create a class to store data for backward indexing
class Backward_Index():
	#declare directory for saving words with it's url
	backward_indexing_dict = {'data':{}}

	def back_indexing(self, name, list_of_words):
		for word in list_of_words:
			if word in self.backward_indexing_dict['data'].keys():
				if name in self.backward_indexing_dict['data'][word]:
					continue
				else:
					self.backward_indexing_dict['data'][word].append(name)
			else:
				self.backward_indexing_dict['data'][word] = []
				self.backward_indexing_dict['data'][word].append(name)
