# Twitter Handle Match Application (Codecademy)
#
# Uses Personality Insights (PI) to analyze the unstructured text (tweets) that 
# of two Twitter handles. PI uses linguistics analytics to infer personality 
# and social characteristics based on 3 models:
# Big Five: describes 5 dimensions of the personality 
# 	(Agreeableness, Conscientiousness, Extraversion, Emotional Range, Openess)
# Needs: Describes what product attributes will resonate well w/ the person
# Values: Describes the factors that will motivate a user's decision making

# a basic interpreter that can handle low level functions of the OS
import sys
# allows arithmetic & comparison functions, such as comparing 2 strings, or multiplying 2 nums
import operator
# makes it easy to make HTTP requests
import requests
# makes it easier to work with JSON objects
import json
# Twitter API
import twitter
# Watson Developer Cloud API
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

#
# API Client Setup
#

# Setup Twitter access/keys
twitter_consumer_key = ''
twitter_consumer_secret = ''
twitter_access_token = ''
twitter_access_secret = ''

# Create Twitter API Client Object
twitter_api = twitter.Api(
	consumer_key=twitter_consumer_key,
	consumer_secret=twitter_consumer_secret,
	access_token_key=twitter_access_token,
	access_token_secret=twitter_access_secret)

# The IBM Bluemix credentials for Personality Insights!
pi_username = ''
pi_password = ''

# Create PI API Client object
personality_insights = PersonalityInsights(
	username = pi_username, 
	password = pi_password)


#
# Functions
#

def analyze(handle):
	"""Analyze the tweets from a given Twitter handle using PI.

	Args:
	    handle (str): The Twitter handle

	Returns:
	    str: Analysis on tweets in JSON

	"""

	# Get the last 200 statuses, ignoring re-tweets, as a list
	statuses = twitter_api.GetUserTimeline(
		screen_name=handle, 
		count=200,
		include_rts=False)

	# We need to send one blob of text to the Personality Insights API for analysis
	text = ""

	# Loop thru the statuses returned and print the Twitter text from each status
	for status in statuses:
		# Only grab tweets written in English
		if (status.lang == 'en'):
			# Concatenate the text encoded into UTF-8 (Twitter text is in Unicode)
			text += status.text.encode('utf-8')

	# Analyze the body of text retrieved from Twitter. Results are in JSON.
	pi_result = personality_insights.profile(text)

	return pi_result

	"""Notes about in operator:

	If it's a string, then in checks for substrings.

	>>> "in" in "indigo"
	True
	>>> "in" in "violet"
	False
	>>> "0" in "10"
	True
	>>> "1" in "10"
	True

	If it's a different kind of iterable (list, tuple, dictionary...), then in checks for membership.

	>>> "in" in ["in", "out"]
	True
	>>> "in" in ["indigo", "violet"]
	False

	In a dictionary, membership is seen as "being one of the keys":

	>>> "in" in {"in": "out"}
	True
	>>> "in" in {"out": "in"}
	False 
	
	"""

def flatten(orig):
	"""Flatten original JSON structure 

	Args:
	    handle (str): PI results in JSON

	Returns:
	    dict: dictionary of traits and percentage

	"""

	# Empty dictionary
	data = {}
	for c in orig['tree']['children']:
		# in operator
		if 'children' in c:
			for c2 in c['children']:
				if 'children' in c2:
					for c3 in c2['children']:
						if 'children' in c3:
							for c4 in c3['children']:
								if (c4['category'] == 'personality'):
									data[c4['id']] = c4['percentage']
						else:
							if (c3['category'] == 'personality'):
								data[c3['id']] = c3['percentage']

	return data

def compare(dict1, dict2):
	"""Compare dictionary keys and store the "distance" between the two keys.

	Args:
	  dict1 (str): Dictonary of traits 
	  dict2 (str): Another dictonary of traits 

	Returns:
	  str: dictionary of keys and distance between the two for a given value 

	"""

	compared_data = {}
	for keys in dict1:
		compared_data[keys] = abs(dict1[keys] - dict2[keys])
	
	return compared_data


#
# Main Program
#

# User 1 Twitter handle processing
user1_handle = "@Codecademy"
user1_results = analyze(user1_handle)
user1 = flatten(user1_results)

# User 2 Twitter handle processing
user2_handle = "@IBM"
user2_results = analyze(user2_handle)
user2 = flatten(user2_results)

# Compare user and celebrity results
compared_results = compare(user1, user2)

# Sort results
sorted_results = sorted(compared_results.items(), key = operator.itemgetter(1))

# Print the top 5 traits that the user handle shares with the celebrity handle
for keys, value in sorted_results[:5]:
	print keys,
	print(user1[keys]),
	print('->'),
	print(user2[keys]),
	print('->')
	print(compared_results[keys])






