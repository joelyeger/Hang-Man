#OOP programing, a decision tree



import math

class Node:

	def __init__(self, data, positive_child = None, negative_child = None):
		"""
		initiate a dot
		:param data
		:param positive_child
		:param negative_child
		"""
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child



class Record:
	def __init__(self, illness, symptoms):
		"""
		initiate a record
		:param illness:
		:param symptoms:
		"""
		self.illness = illness
		self.symptoms = symptoms
	
			
def parse_data(filepath):
	"""
	creats Record objects out of information from file
	:param filepath:
	:return: list of Record objects
	"""
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records
		
		
class Diagnoser:
	def __init__(self, root):
		"""
		initiate a Diagnoser
		:param root: a Node object
		"""
		self.root = root
		
	def diagnose(self, symptoms):
		"""
		diagnose an illness according to symptoms
		:param symptoms:
		:return: illness
		"""
		current = self.root
		while current.positive_child != None and current.negative_child != None:
			if current.data in symptoms:
				current = current.positive_child
			else:
				current = current.negative_child
		return current.data
		
	def calculate_success_rate(self, records):
		"""
		calculate success rate of a tree
		:param records:
		:return: success rate
		"""
		if records == []:
			return 1
		correct = 0
		general = len(records)
		for record in records:
			cur = self.root
			while cur.positive_child != None and cur.negative_child != None:
				if cur.data in record.symptoms:
					cur = cur.positive_child
				else:
					cur = cur.negative_child
			if cur.data == record.illness:
				correct += 1
		return correct / general
		
	def all_illnesses(self):
		"""
		:return: a list of all the illnesses in the tree
		"""
		illnesses_amount = []
		if self.root.positive_child.positive_child != None or self.root.positive_child.negative_child != None:
			pos_child = Diagnoser(self.root.positive_child).all_illnesses()
			illnesses_amount.extend(pos_child)
		if self.root.negative_child.positive_child != None or self.root.negative_child.negative_child != None:
			neg_child = Diagnoser(self.root.negative_child).all_illnesses()
			illnesses_amount.extend(neg_child)
		if self.root.positive_child.positive_child == None and self.root.positive_child.negative_child == None:
			illnesses_amount.append(self.root.positive_child.data)
		if self.root.negative_child.positive_child == None and self.root.negative_child.negative_child == None:
			illnesses_amount.append(self.root.negative_child.data)

		final_lst = []
		for i in illnesses_amount:
			if final_lst == []:
				final_lst.append(i)
			else:
				for k in final_lst:
					if i in final_lst:
						break
					else:
						if illnesses_amount.count(i) >= illnesses_amount.count(k):
							final_lst.insert(final_lst.index(k), i)
						elif final_lst[-1] == k:
							final_lst.append(i)

		return final_lst

	def paths_to_illness(self, illness, cur_path=[]):
		"""
		checks all possible paths to an illness
		:param illness:
		:param cur_path:
		:return: all paths to an illness
		"""
		final_lst = []
		if self.root.positive_child == None and self.root.negative_child == None:
			if illness == self.root.data and cur_path != []:
				final_lst.append(cur_path)
			else:
				return []

		if self.root.positive_child != None:
			pos_path = cur_path[:] + [True]
			pos_child = Diagnoser(self.root.positive_child).paths_to_illness(illness, pos_path)
			if pos_child != []:
				final_lst.extend(pos_child)

		if self.root.negative_child != None:
			neg_path = cur_path[:] + [False]
			neg_child = Diagnoser(self.root.negative_child).paths_to_illness(illness, neg_path)
			if neg_child != []:
				final_lst.extend(neg_child)

		return final_lst




def build_tree(records, symptoms, count = 0, path = []):
	"""
	build a choices tree that diagnose illnesses
	:param records:
	:param symptoms:
	:param count:
	:param path:
	:return: a Diagnoser object
	"""
	if symptoms != []:
		if records != []:
			if len(symptoms) > count:
				return Node(symptoms[count], build_tree(records, symptoms, count + 1, path + [True]),
									   build_tree(records, symptoms, count + 1, path + [False]))
			else:
				list_of_symptoms = []
				for i in range(count):
					if path[i]:
						list_of_symptoms.append(symptoms[i])
					else:
						list_of_symptoms.append('not ' + symptoms[i])
				dict_of_summary = {}
				for record in records:
					if record.illness in dict_of_summary:
						counter_symptoms = dict_of_summary[record.illness]
					else:
						counter_symptoms = 0
					counter = 0
					for symptom in list_of_symptoms:
						if 'not' in symptom:
							if symptom[4:] in record.symptoms:
								continue
							counter += 1
						if symptom not in record.symptoms:
							continue
						counter += 1

					if counter == len(list_of_symptoms):
						counter_symptoms += 1
						dict_of_summary[record.illness] = counter_symptoms
					else:
						dict_of_summary[None] = counter_symptoms
				lst_of_sumarry_sorted = list({k: v for k, v in sorted(dict_of_summary.items(), key=lambda item: item[1])})

				return Node(lst_of_sumarry_sorted[-1])

	else:
		if records != []:
			return Node(records[0].illness)

	if records == [] and symptoms == []:
		return Node(None)

def combinations(iterable, r):
	"""
	checks all combination in the length of r out of iterable
	:param iterable:
	:param r:
	:return: an iterator of all combinations
	"""
	pool = tuple(iterable)
	n = len(pool)
	if r > n:
		return
	indices = list(range(r))
	yield list(pool[i] for i in indices)
	while True:
		for i in reversed(range(r)):
			if indices[i] != i + n - r:
				break
		else:
			return
		indices[i] += 1
		for j in range(i + 1, r):
			indices[j] = indices[j - 1] + 1
		yield list(pool[i] for i in indices)


def this_choose_that(this, that):
	"""
	calculate a binomial coefficient
	:param this:
	:param that:
	:return: binomial coefficient
	"""
	return (math.factorial(this) / (math.factorial(that) * math.factorial(this - that)))

def optimal_tree(records, symptoms, depth):
	"""
	build a tree with a depth given which has the highest success rate
	:param records:
	:param symptoms:
	:param depth:
	:return: a Diagnoser object
	"""
	if len(symptoms) == depth:
		return build_tree(records, symptoms)
	else:
		iter_tool = combinations(symptoms, depth)
		dict_of_options = {}
		for option in range(int(this_choose_that(len(symptoms), depth))):
			current_iter = iter_tool.__next__()
			dict_of_options[build_tree(records, current_iter)] =\
				Diagnoser(build_tree(records, current_iter)).calculate_success_rate(records)
		lst_of_options_sorted = list({k: v for k, v in sorted(dict_of_options.items(), key=lambda item: item[1])})
		return lst_of_options_sorted[-1]






