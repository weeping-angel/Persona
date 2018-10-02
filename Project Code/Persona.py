from flask import render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from models import *
from flask import request
from maal import get_tweets, get_instas, get_emotion, get_recom

#default general data (in case no data is obtained)
mood="Nice day, isn't it?"
emotion='joy'
score_card=[0, 18.885392, 0, 3.4337739999999997, 1.802328, 3.161688, 0] 

@app.route('/', methods = ['GET', 'POST'])
@app.route('/home', methods = ['GET', 'POST'])
def home():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			return redirect(url_for('dashboard',name=user.username,email=user.email,twitter_account=user.twitter,instagram_account=user.instagram))
		else:
			flash('Login failed !!!','danger')
	return render_template('index.html', form=form)
	
@app.route('/register' , methods = ['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password, twitter=form.twitter.data, instagram=form.instagram.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Account Created for {form.username.data}!', 'success')
		return redirect(url_for('home'))
	return render_template('register.html', form=form, title='Register')
	
@app.route('/dashboard/<name>/<email>/<twitter_account>/<instagram_account>', methods = ['GET', 'POST'])
def dashboard(name,email,twitter_account,instagram_account):
	global mood
	global emotion
	global score_card
	days = 1
	if request.method == 'POST':
		days = int(request.form['timeline'])
		tweets = get_tweets(twitter_account, days)
		instas = get_instas(instagram_account, days)
		if (len(tweets) + len(instas)) != 0 : emotion,score_card = get_emotion(tweets, instas)
		dict = { 'anger' : 'Calm Down. It seems Someone had a bad day.' , 'sadness': 'Cheer up! Every cloud has a silver lining.', 'fear': "Don't be scared. Everythings gonna be alright.", 'analytical': 'Its good to be analytical.', 'joy': "Nice day. isn't it?", 'confident' : 'You are looking an inch taller', 'tentative' : 'Go with what your heart says.' }
		mood = dict[emotion]
		return render_template('dashboard.html', name=name, twitter_account=twitter_account, instagram_account=instagram_account, title='Dashboard', mood=mood, emotion=emotion)
	return render_template('dashboard.html', name=name, twitter_account=twitter_account, instagram_account=instagram_account, title='Dashboard', mood=mood, emotion=emotion)

@app.route('/recommend/')
def recommend():
	global emotion
	global score_card
	videos, images, articles, songs = get_recom(score_card)
	return render_template('recommendations.html',videos=videos,songs=songs, articles=articles, images=images)
	
if __name__ == '__main__':
	app.run(debug=True)