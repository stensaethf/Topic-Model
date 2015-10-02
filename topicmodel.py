'''
- topicmodel.py
- Frederik Roenn Stensaeth, 09.15.2015
- A short Python program that takes in a text file and tries to find the most
  important words in the file.
 
- Credit:
  The 50 out of the 53 words (the first 50) in the common_words list were
  found at https://www.englishclub.com/vocabulary/common-words-100.htm (Endlish
  Club). These 50 words were found to be the most common English words in
  writing globally.
'''

import sys
from operator import itemgetter

# 50 most common written English words globally according to the English Club
# and 'is', 'am' and 'has'.
common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', \
                'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', \
                'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', \
                'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', \
                'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', \
                'about', 'who', 'get', 'which', 'go', 'me', 'is', 'am', 'has']

def recordFrequencies(f):
   """
   recordFrequencies() records the number of times a word has been mentioned
   in a given file and stores the results in a dictionary. Returns this
   dictionary.

   @params: filename.
   @return: dictionary with words as keys and frequency counts as values.
   """

   words = {}
   for line in f:
      for word in line.split():
         # Removes invalid letter from end of word ('!', '.', ',', etc.).
         if ord(word[-1]) < 97 or ord(word[-1]) > 122:
            word = word[:-1]

         # Records/ updates the frequency of a word.
         if word in words:
            words[word] += 1
         else:
            words[word] = 1

   return words

def findCapitalized(words):
   """
   findCapitalized() finds the words that are capitalized in a dictionary (keys
   are words). Capitalized words and their values are moved to a separate
   dictionary and removed from the original dictionary. The new dictionary and
   the updated one are returned.

   @params: dictionary with words as keys.
   @return: dictionary containing the words that were capitalized in the param
            dictionary and param dictionary w/o the capitalized words.
   """

   words_capitalized = {}
   words_update = words.copy()
   for w in words:
      if w == w.capitalize():
         # If w is capitalized, check if it only appears capitalized. Given
         # a certain length of text this would provide a decent benchmark for
         # whether it is a name, title, etc - which would probably be
         # important.
         if w.lower() not in words:
            words_capitalized[w] = words[w]
            words_update.pop(w, None)
         else:
            # The word was not only mentioned in a capitalized form, so we add
            # the frequencies together and remove the capitalized form from the
            # dictionary.
            words_update[w.lower()] = words_update[w.lower()] + words_update[w]
            words_update.pop(w, None)

   # Sorts the capitalized words found by frequency.
   capitalized_sorted = sortDictionaryByFrequency(words_capitalized)

   return words_update, capitalized_sorted

def findNumbers(words):
   """
   findNumbers() finds the numbers in a dictionary (keys are words/numbers).
   Numbers and their values are moved to a separate dictionary and removed from
   the original dictionary. Returns both the new and the updated dictioaries.

   @params: dictionary with words as keys.
   @return: dictionary containing the numbers that were in the param dictionary
            and param dictionary w/o the numbers found.
   """

   digits = {}
   words_update = words.copy()
   for w in words:
      if w.isdigit():
         # Checks if w is a number. If it is a number we add it to the digits
         # dictionary. Need to remove the number from the orginzal dictionary,
         # as it is now recorded in the digits dictionary instead.
         digits[w] = words[w]
         words_update.pop(w, None)
   
   # Sorts the numbers in the digits dictionary by their frequencies.
   digits_sorted = sortDictionaryByFrequency(digits)

   return words_update, digits_sorted

def sortDictionaryByFrequency(d):
   """
   sortDictionaryByFrequency() sorts a dictionary's keys by their value 
   (frequency in this case). Sorted keys are recorded in a list. Returns the
   list of sorted dictionary keys.

   @params: dictionary with frequencies as values.
   @return: list with the keys of the param dictionary sorted by highest to
            lowest frequency counts.
   """

   sorted_list = []
   # Sorts the keys in the dictionary by their values. And add them to a new
   # list. Highest to lowest freuquency.
   for t in sorted(d.items(), key=itemgetter(1), reverse=True):
      sorted_list.append(t[0])

   return sorted_list

def filterByCommonWords(lst):
   """
   filterByCommonWords() finds all words that are not 'common' (50 most used
   English words used in writing globally according to the English Club in
   addition to 'is', 'am' and 'has') in a list and makes a new list containing
   these 'uncommon' words. Returns the list of 'uncommon' words.

   @params: list of words.
   @return: list of words from the param list that are not present in the
            hardcoded list of common words.
   """

   filtered_list = []
   # Checks if the word is 'common'. Only adds 'uncommon' words to the
   # after-filtered list.
   for i in lst:
      if i.lower() not in common_words:
         filtered_list.append(i)

   return filtered_list

def findImportant(words, capitalized, numbers, maxLength):
   """
   findImportant() combines lists of words, capitalized words and numbers into
   one large list and divides this list by the number of words that are
   desired. The combined list is made by treating capitalized words as most
   important, then numbers and finally uncapitalized 'uncommon' words.

   @params: lists of words, capitalized words and numbers and max length num.
   @return: list of 'important' words given the provided lists and desired
            number of words.
   """

   # Combines the lists provided in the order of importance (as the author has
   # implemented it).
   combined_words = capitalized + numbers + words
   # Chooses only the first n words, decided by maxLength provided.
   important_words = combined_words[:maxLength]

   return important_words

def bestWords(f, maxLength):
   """
   bestWords() finds the maxLength most important words in a file. important
   words are found by looking at whether they are capitalized in the file,
   whether it is a number and whether they are 'uncommon' (not common according
   to the English Club).

   @params: filename and number representing desired number of 'important'
            words requested.
   @return: list of 'important' words.
   """

   # Finds the frequencies with which capitalized words, numbers and 'uncommon'
   # words are mentioned in the text file. Then finds the most important ones.
   words = recordFrequencies(f)
   words, numbers = findNumbers(words)
   words, words_capitalized = findCapitalized(words)
   words_sorted = sortDictionaryByFrequency(words)

   filt_cap = filterByCommonWords(words_capitalized)
   filt_words = filterByCommonWords(words_sorted)

   best_words = findImportant(filt_words, filt_cap, numbers, maxLength)

   return best_words

def main():
   if len(sys.argv) != 2:
      sys.exit()
   try:
      f = open(sys.argv[1])
      for word in bestWords(f, 5):
         print(word)
      f.close()
   except:
      print("Error. Please check whether the file provided is valid.")
      sys.exit()

if __name__ == '__main__':
   main()