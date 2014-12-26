# Author:Vipul Raheja

import os
import re
import collections
import itertools
import random

DICT1 = '/usr/share/dict/words'
DICT2 = 'wordsEn.txt'
VOWELS = 'aeiou'
alphabet = 'abcdefghijklmnopqrstuvwxyz'

# Handle Duplicates in Strings
""" Generates all possible words from the ones containing multiple
	continuous duplicate letters. Continuous duplicate letters are 
	replaced by one and two letters.
	sheeeeeeeep = ['shep','sheep']
	jjoooob = ['job', 'jjob', 'joob', 'jjoob']
"""
def generate_duplicate_candidates(word):
	charlist = [[word[0], 1]]
	for k in xrange(1, len(word)):
		if word[k] == word[k-1]:
			if charlist[-1][0] == word[k]:
				charlist[-1][1] += 1
			else:
				charlist += [[word[k], 2]]
		else:
			charlist += [[word[k], 1]]

	duplicate_charlist = list(c for c in charlist if c[1] > 1)

	permuted_charlist = []
	permuted_count = itertools.product("12", repeat = len(duplicate_charlist))
	for permutation in permuted_count:
		currstr = ""
		k = 0
		for char in charlist:
			if char[1] > 1:
				currstr += str(char[0])*int(permutation[k])
				k += 1
			else:
				currstr += char[0]
		permuted_charlist += [currstr]

	# for i in xrange(0, len(word)):
	# 	word1 = str(word[:i] + word[i] + word[i:])
	# 	word2 = str(word[:i] + word[i] + word[i] + word[i:])
	# 	if word1 not in permuted_charlist:
	# 		permuted_charlist += [word1]
	# 	if word2 not in permuted_charlist:
	# 		permuted_charlist += [word2]

	return permuted_charlist

# Handle Vowel Replacements
""" Generates all possible words from the ones containing vowels.
	Vowels are replaced by other vowels.
	job = ['jab','jeb', 'jib', 'jub']
"""
def replace_vowels(words, dictionary):
	replaces = []
	for word in words:
		vowelind = list(x for x in xrange(0, len(word)) if word[x] in VOWELS)
		vowel_combinations = itertools.product("aeiou", repeat = len(vowelind))

		for combination in vowel_combinations:
			currstr = ""
			l = 0
			for k in xrange(0, len(word)):
				if word[k] in VOWELS:
					currstr += combination[l]
					l += 1
				else:
					currstr += word[k]

			if currstr not in replaces and currstr != word:
				replaces += [currstr]

	return replaces


def generate_misspelling(word):
	misspells = []

	"""
	Create up to 3 duplicates of each letter
	"""
	duplicates = []
	for i in xrange(0, len(word)):
		duplicates += [str(word[:i] + word[i] + word[i:])]
		duplicates += [str(word[:i] + word[i] + word[i] + word[i:])]

	"""
	Create vowel replacements
	"""
	vowelswords = []
	for i in xrange(0, len(word)):
		if word[i] in VOWELS:
			tempword = word
			for v in VOWELS:
				if v != tempword[i]:
					tempword = list(tempword)
					tempword[i] = v
					tempword = "".join(tempword)
					if tempword not in vowelswords:
						vowelswords += [tempword]

	capitalwords = []
	"""
	Randomly generate 10 words with arbitrary letters capitalized
	"""
	for i in range(10):
		num_capitals = random.sample(range(1, len(word)), 1)
		set_capitals = random.sample(range(0, len(word)), num_capitals[0])
		capital = word
		capital = list(capital)
		for i in xrange(0, len(word)):
			if i in set_capitals:
				capital[i] = capital[i].upper()
		capital = "".join(capital)
		capitalwords += [capital]

	misspells = duplicates + vowelswords + capitalwords

	return misspells

def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word, dictionary):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in dictionary)

def known(words, dictionary): return set(w for w in words if w in dictionary)

def create_dictionary(filename):
	"""
	Create dictionary of words from file

	"""
	word_set = set()
	if os.path.isfile(filename):
		with open(filename, 'r') as f:
			for line in iter(f):
				word_set.add(line.strip('\n'))
	else:
		print "File not found!"
	return word_set

def replacement_cost(repl, word):
	current_word = 0
	for i in xrange(len(repl)):
		if len(repl) > i and len(word) > i and repl[i] != word[i]:
			current_word += 1
	return current_word


"""
USAGE: 
	1. To simply get a correct spelling: 
		$> <enter_word>
	2. To check possible misspells and see if no "NO_SUGGESTION" is output:
		$> <enter_word> -c
"""
def main():
	dictionary = create_dictionary(DICT1)
	dict2 = create_dictionary(DICT2)

	while True:
		word = raw_input('> ')
		check = False
		found = False
		word = word.lower()


		"""
		Checking mode: to generate misspells and verify there is no NO_SUGGESTION
		"""
		if "-c" in word:
			check = True
			misspells = generate_misspelling(word.split()[0])
			print "MISSPELL\tSUGGESTED SPELLING (IF ANY)"
			print "------------------------------------------"
		else:
			misspells = [word]

		for word in misspells:
			found = False
			if check is True:
				print word + "\t",

			word = word.lower()

			"""
			Generate duplicates and check if they exist in dictionary
			"""
			duplicates = generate_duplicate_candidates(word)
			# print duplicates
			for candidate in duplicates:
				if candidate in dictionary:
					print candidate
					found = True
					break

			"""
			Generate vowel replacaments and check if they exist in dictionary
			"""	
			if found is False:
				for candidate in duplicates:

					replaces = replace_vowels(duplicates, dictionary)
					# print replaces

					"""		
					Check for replacements in duplicates 
					To handle cases like sheeueueuep for sheep
					"""
					edits = edits1(word)
					for r in replaces:

						duplicates = generate_duplicate_candidates(r)
						# print duplicates
						for candidate in duplicates:
							if candidate in dictionary:
								print candidate
								found = True
								break
						if found is True:
							break

					if found is True:
						break						


					"""
					Fine tuning for getting the best spelling from vowel replaces
					Measure edit distance of each candidate 
					"""
					# print replaces
					# print len(replaces)
					replaces_weight = []
					for repl in replaces:
						replaces_weight += [replacement_cost(repl, word)]

					# replaces_weight = list(len([i for i in xrange(len(repl)) if repl[i] != word[i]]) for repl in replaces)
					min_weight = min(replaces_weight)
					# print replaces_weight
					
					# print min_weight
					# print replaces

					candidates = []
					candidate_wts = []
					for candidate in replaces:
						if candidate in dictionary:
							candidates += [candidate]
							candidate_wts += [replaces_weight[replaces.index(candidate)]]

					# print candidates
					# print candidate_wts

					"""
					More fine tuning - verify with another dictionary
					or
					Get the first candidate with minimum edit distance
					"""
					if len(candidates) == 1:
						print candidates[0]
						found = True
						break

					else:
						for candidate in candidates:
							# print dict2
							# print (candidate_wts[candidates.index(candidate)]) 
							if candidate in dict2:
								print candidate
								found = True
								break
							elif candidate_wts[candidates.index(candidate)] == min_weight:
								print candidate
								found = True
								break

					if found is True:
						break

				"""
				Edit distance based approach
				Find words within edit distance of 2
				Based on Norvig's implementation of spell checker
				This is because otherwise, this spell checker focuses solely on 
				vowel changes and duplicates
				""" 
				# if found is False:
				# 	editwords = list(known([word], dictionary) or known(edits1(word), dictionary) or known_edits2(word, dictionary))
				# 	edit_val = []
				# 	for w in editwords:
				# 		edit_val += [replacement_cost(w, word)]
				# 	# print edit_val

				# 	for w in editwords:
				# 		if edit_val[editwords.index(w)] <= 2:
				# 			print w
				# 			found = True
				# 			break

			if found is False:
				print "NO_SUGGESTION"

if __name__ == "__main__":
	main()
