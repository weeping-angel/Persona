import twitter
import time
import datetime
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import json
from watson_developer_cloud import ToneAnalyzerV3
from keras.models import Sequential
from keras.models import load_model
import numpy
import random
import csv

CONSUMER_KEY = 'kEBZuh53jExPoXec2nzJemVyp'
CONSUMER_SECRET = 'uVvVVQMYfFBWtqEkiQNe5gKAFFvgFJ7omk2AUOSh91OknyHE76'
ACCESS_TOKEN = '1044563858239631365-LMExPSXn24FHOZ3p6JFBwdzPb91NhW'
ACCESS_TOKEN_SECRET = '9aQLjxeDRmq0LUoUUS5aHr5GiZVirRxxggeVFPTfQoMTW'

#emotions
emots = ['motivational','funny','productivity','calm']
#types
v = 'videos'
im = 'images'
a = 'articles'
sg = 'songs'

def get_tweets(id,max_days = 1):
	api = twitter.Api(consumer_key=CONSUMER_KEY,
					  consumer_secret=CONSUMER_SECRET,
					  access_token_key=ACCESS_TOKEN,
					  access_token_secret=ACCESS_TOKEN_SECRET)

	try: 
		tweets = api.GetUserTimeline(screen_name=id)
	except Exception:
		return []
	latest=[]
	current = datetime.utcnow();
	for t in tweets:
		ts = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(t.created_at,'%a %b %d %H:%M:%S +0000 %Y')),'%Y-%m-%d %H:%M:%S')
		days = (current-ts).days
		if(days<=max_days):
			d = t.text
			d = ' '.join(word for word in d.split() if not word.startswith('http'))
			latest.append(d)
	return latest;



def time_from_timestamp(stamp):
	posix_time = int(stamp)
	return datetime.utcfromtimestamp(posix_time)

def get_instas(id,max_days = 1):	
	r = requests.get("https://www.instagram.com/"+id+"/")
	data = r.text
	current = datetime.utcnow();
	soup = BeautifulSoup(data,features='html.parser')
	i=1
	latest = []
	for link in soup.find_all('script'):
		if str(link.text).startswith('window._sharedData'):
			t=(link.text[21:]);
			t = t[:len(t)-1]
			object = json.loads(t)
			nodes = object['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
			for n in nodes:
				ts = time_from_timestamp(n['node']["taken_at_timestamp"]);
				days = (current - ts).days;
				if days <= max_days:
					latest.append(n['node']['edge_media_to_caption']['edges'][0]['node']['text'])				
	return latest


def get_emotion(tweets,instas):
	service = ToneAnalyzerV3(username='196f795f-ea34-4306-85f9-081ee4b25117',password='aN8dsxyipDLi',version='2017-09-21')
	score_card={'anger':0, 'joy':0, 'sad':0, 'tentative':0, 'confident':0, 'analytical':0, 'fear':0}
	for tweet in tweets:
		tweet = tweet.encode('utf-8')
		result = json.dumps(service.tone(tone_input=str(tweet), content_type="text/plain", text=str(tweet)).get_result(), indent=2)
		result = json.loads(result)
		try:
			emotion = str(result['document_tone']['tones'][0]['tone_id'])
			score = float(result['document_tone']['tones'][0]['score'])
			score_card[emotion]+=score
		except Exception:
			continue
	
	for insta in instas:
		insta = insta.encode('utf-8')
		result = json.dumps(service.tone(tone_input=str(insta), content_type="text/plain", text=str(insta)).get_result(), indent=2)
		result = json.loads(result)
		try: 
			emotion = str(result['document_tone']['tones'][0]['tone_id'])
			score = float(result['document_tone']['tones'][0]['score'])
			score_card[emotion]+=score
		except Exception:
			continue
		
	final_emotion = max(score_card,key=score_card.get)
	return final_emotion, list(score_card.values())

	
def sigmoid(w,x):
	return 1/(1+numpy.exp(-(w*x)))

def test(data):
	print(data)
	model = load_model('hack2.h5')
	res = sigmoid([10,10,10,10],model.predict(numpy.array([data]))[0]);
	for i in range(len(res)):
		if(res[i]>0.8):
			res[i] = 1;
		else:
			res[i] = 0;
	return res;
	
def read_csv(emotion,dtypes):
	sets=[]
	try:
		csvFile = open('csv/'+emotion+'/'+dtypes+'.csv', 'r')
		reader = csv.reader(csvFile)
		n=0
		for row in reader:
			n+=1;
		rands = random.sample(range(0,n),3)
		i=0;
		csvFile.seek(0);
		reader = csv.reader(csvFile)
		for row in reader:
			if i in rands:
				sets.append(row[0])
			i+=1
	except Exception:
		pass
	return sets;

def get_recom(score):#returns list of list with structure [[videos links][images links][articles links][song links]] 		
	res = test(score); # if the person is having 2 emotions like funny and motivational simultaneously then instead of 3 ,6 elements will be their in each list  
	videos = []
	images = []
	articles = []
	songs = []
	i=0
	for r in res:
		if r == 1:
			print(emots[i])#prints result 4 size emotion , can be commented
			videos.append(read_csv(emots[i],v))
			images.append(read_csv(emots[i],im))
			articles.append(read_csv(emots[i],a))
			songs.append(read_csv(emots[i],sg))
		i+=1
	videos = list(numpy.array(videos).flatten())
	images = list(numpy.array(images).flatten())
	articles = list(numpy.array(articles).flatten())
	songs = list(numpy.array(songs).flatten())
	return videos,images,articles,songs