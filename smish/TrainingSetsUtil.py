"""
TrainingSetsUtil.py acceses the dataset containing all the messages.
It detemines the relative frequency of each and every word in the mesaage
and divides the dataset in 2 files Spam_training_set.csv and
ham_training_set.csv which containg the words and their frequencies from
the respective categories. 
"""
#import statements
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# for tokenize
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import ConfigParser

# for reading all the files
from os import listdir
from os.path import isfile, join

# add path to NLTK file
nltk.data.path = ['nltk_data']

# load stopwords
stopwords = set(stopwords.words('english'))

#open dataset
from xlrd import open_workbook
wb = open_workbook('data.xlsx')
for s in wb.sheets():
    values = []
    for row in range(1,s.nrows):
		value  = (s.cell(row,0).value)
		try : value = str((value))
		except : pass
		value1 = (s.cell(row,1).value)
		try : value1 = str((value1))
		except : pass
		temp = [value, value1]
		values.append(temp)


def get_words(message):
    all_words = set(wordpunct_tokenize(message.replace('=\\n', '').lower()))
    # remove the stopwords
    msg_words = [word for word in all_words if word not in stopwords and len(word) > 2]
    return msg_words
       
def make_training_set(category):
    
    """
    Returns a dictionary of <term>: <occurrence> of all 
    the terms in files contained in the directory specified by path.
    occurrence is the percentage of documents that have the 'term' in it.
    frequency is the total number of times the 'term' appears across all the
    documents in the path
    """
    # initializations
    training_set = {}

    other_count = 0
    # total number of files in the directory
    total_msg_count = len(values)
    
    for i in range(0, len(values)):
        
        if values[i][1] != category:
            other_count += 1
            continue
    
        message = values[i][0]
        
        # we have the message now
        # get the words in the message
        terms = get_words(message)
                    
        # what we're doing is tabulating the number of messages
        # that have the word in them
        # add these entries to the training set
        for term in terms:
            if term in training_set:
                training_set[term] = training_set[term] + 1
            else:
                training_set[term] = 1
    
    # reducing the count of other msgs from msg count
    total_msg_count -= other_count
    # calculating the occurrence for each term
    for term in training_set.keys():
        training_set[term] = float(training_set[term]) / total_msg_count
                            
    return training_set

print ''    
print 'Loading training sets...',
spam_training_set = make_training_set("spam")
ham_training_set = make_training_set("ham")

with open('spam_training_set.csv', 'wb') as f_output:
	csv_output = csv.writer(f_output, delimiter=',', quotechar='|')
	csv_output.writerow(["term", "freq"])
	for term in spam_training_set : 
		row = []
		row.append(term)
		row.append(spam_training_set[term])
		csv_output.writerow(row)

with open('ham_training_set.csv', 'wb') as f_output:
	csv_output = csv.writer(f_output, delimiter=',', quotechar='|')
	csv_output.writerow(["term", "freq"])
	for term in ham_training_set : 
		row = []
		row.append(term)
		row.append(ham_training_set[term])
		csv_output.writerow(row)
	
print 'done.'
print ''