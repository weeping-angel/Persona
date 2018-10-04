from maal import *
from models import *
from EmailSystem import *
import datetime
import time

users = User.query.all()
threshold = 0.5
Flag = True
while True:
	l=datetime.datetime.now()
	if l.hour == 18 and Flag: # Run everyday at 18:00
		for user in users:
			email = user.email
			twitter = user.twitter
			instagram = user.instagram
			
			tweets = get_tweets(twitter,1)
			instas = get_instas(instagram,1)
			
			emotion, score_card = get_emotion(tweets, instas)
			dominant_emotion_score = max(score_card)
			if dominant_emotion_score >= threshold:
				videos, images, articles, songs = get_recom(score_card)
				e = Email(email)
				
				email_body = '\n Recommended Videos \n\n'
				for video in videos: 
					email_body+=str(video)
					email_body+='\n'
				email_body += '\n Recommended Songs \n\n'
				for song in songs: 
					email_body+=str(song)
					email_body+='\n'
				email_body += '\n Recommended Articles \n\n'
				for article in articles: 
					email_body+=str(article)
					email_body+='\n'
				email_body+= "\n\n For more recommendations, visit our website : Persona \n\n"
					
				for i in range(0,len(images)):
					images[i] = 'static\\' + images[i]
				print(images)
				e.send_mssg(email_body,images)
		Flag = False
	else:
		Flag = True
		
	
	
