import os
import time
import tweepy
import pandas as pd
import numpy as np
from datetime import datetime


consumer_key = 'insertyours'
consumer_secret = 'insertyours'
access_token = 'insertyours'
access_token_secret = 'insertyours'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

tweets = []
now = datetime.now()
name = 'gabrielboric'
text_query = ''


def queryToCsv(text_query):
    try:
    	#Download tweets 
        print('Downloading tweets for ' + name + '...')
        tweets_list = [[tweet.id, tweet.created_at, tweet.full_text] for tweet in tweepy.Cursor(api.user_timeline, screen_name=name, tweet_mode="extended").items()]
        #tweets_list = [[tweet.id, tweet.created_at, tweet.full_text] for tweet in api.user_timeline(screen_name=name,  tweet_mode = 'extended')]
        # Creat dataframe to save into csv file
        tweets_df = pd.DataFrame(tweets_list, columns=['ID', 'Datetime', 'Text'])        
        date = now.strftime("%m%d%Y-%H%M%S")
        filename = name+date
        tweets_df.to_csv(filename+'{}-tweets.csv'.format(text_query), sep=',', index=False)

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)

    else:
    	print('Tweets downloaded')

	
def checkFile():
	try:
		# Check if there are files for the username, sort them by date and check the last one	
		file_exists = [filename for filename in os.listdir('.') if filename.startswith(name)]
		file_sorted = [file for file in sorted(file_exists, key=os.path.getmtime)]	
		file_dates = [os.path.getctime(filename) for filename in os.listdir('.') if filename.startswith(name)]
		dates_sorted = sorted(file_dates)
		data1 = pd.read_csv(file_sorted[-1], sep=',')
		data2 = pd.read_csv(file_sorted[-2], sep=',')
		print('Found files for ' + name +':')
		#print('Last file: ', data1)
		#print('Second to last file: ', data2)
		#See if something changed and show changes
		changed = pd.concat([data1,data2], axis=0)
		change = changed.drop_duplicates(keep=False)
		if change.empty:
			print('Nothing changed')
		else:
			print('This changed: ', change)
		
		#If it's on change but not in data1 then it's a deleted tweet
		deleted = change.isin(data1) 

		if False in deleted.values:
			print('Found a deleted tweet')
		else:
			print('No tweets were deleted')

	except IndexError:
		print('There are no files for ' + name)

	finally:
		print('Done checking files')

	

queryToCsv(text_query)
checkFile()

