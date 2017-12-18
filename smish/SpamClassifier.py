"""
SpamClassifier.py takes as input the text message that is recieved by the mobile client.
It applies naive bayes on the message the compares its spam and ham probabilites.
Whichever is greater, it returns that as the answer.
"""
import csv
# for tokenize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import ConfigParser
# for reading all the files
from os import listdir
from os.path import isfile, join

def csv_reader(file_obj):
	training_set = {}
	reader = csv.reader(file_obj)
	for row in reader:
			training_set[row[0]] = row[1]
	return training_set

# add path to NLTK file
nltk.data.path = ['nltk_data']
# load stopwords
stopwords = set(stopwords.words('english'))
#from TrainingSetsUtil import *
import ConfigParser
# c is an experimentally obtained value
def get_words(message):
    all_words = set(wordpunct_tokenize(message.replace('=\\n', '').lower()))
    msg_words = [word for word in all_words if word not in stopwords and len(word) > 2]
    return msg_words

# c is an experimentally obtained value
def classify(message, training_set, prior = 0.5, c = 3.7e-4):
  
    msg_terms = get_words(message)
    msg_probability = 1
    for term in msg_terms:
        if term in training_set:
			msg_probability *= float(training_set[term])
        else:
            msg_probability *= c
            
    return float(msg_probability) * prior

def func(sms) :
	spam_training_set = {}
	with open("spam_training_set.csv", "rb") as f_obj:
			spam_training_set = csv_reader(f_obj)
	#print spam_training_set
	ham_training_set = {}
	with open("ham_training_set.csv", "rb") as f_obj:
			ham_training_set = csv_reader(f_obj)
	#print ham_training_set

	# 0.07 and 0.93 because the ratio of samples for spam and ham were the 0.2-0.8
	spam_probability = classify(sms, spam_training_set, 0.07)
	ham_probability = classify(sms, ham_training_set, 0.93)
	#print 'spam_probability : ', spam_probability
	#print 'ham_probability : ', ham_probability
	if spam_probability > ham_probability:
		return "SPAM"
	else:
		return "HAM"
	print ''