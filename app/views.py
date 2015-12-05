from app import app
import fitbit
import ConfigParser
import requests
import oauth2
import urlparse
from flask import render_template, request, send_from_directory
import datetime
import facebook

from time import gmtime, strftime


consumer_key='709255b3ccd60926243482557587190e'
client_secret='9afc51333f6623a126190800349a57d7'
resource_owner_key='39673cbdee35eb5b8f6be194fb7fcce6'
resource_owner_secret='c0f2698570f4a83592992f9d7b3d627f'

#client2=fitbit.Fitbit(consumer_key, client_secret, resource_owner_key = resource_owner_key, resource_owner_secret = resource_owner_secret)
#print client2._COLLECTION_RESOURCE('activities')

start_time = 0

@app.route('/')
@app.route('/index')
def index():
    #content = requests.get('https://api.fitbit.com/1/user/-/activities/steps/date/today/1m.json')
    #print content.json()
    user = {'nickname': 'Ionel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/start-training-action')
def start_training_action():
    print 'function called'
    global start_time
    #start_time = datetime.datetime.now()
   
    start_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #print start_time


    attachment =  {
    	'name': 'Save the Children',
    	'link': 'http://www.cheamcc.co.uk/stumping/wp-content/uploads/2014/04/stc.jpg',
    	'caption': 'Donate for Save the Children organization',
    	'description': 'Lets make the world better. Donate and help a lot of people.',
    	'picture': 'http://www.cheamcc.co.uk/stumping/wp-content/uploads/2014/04/stc.jpg'
    }
    graph = facebook.GraphAPI('CAAOFsL4kRvkBAG7s3VF29TX7iPZB2CzRZAn2BeIqZBaDtjBd6wtQFWe72YR8i51MSDfmAH0eX7FfBmSaGT1PiPw1Y7HJ4xtWMVhpNOoOh44Yy1TYeucQPQSS9GVTsC7UjpbRBK7Wd3fqZAQVVlHb6DKSal04eYqm0iJLWt3QtjXG0MEVQ80FdYzB9DRqAHzcJNR5O9hfZCzAkG0yFJDGt8pE7ZBsvoZBcAZD')
    profile = graph.get_object('me')
    txt = 'Today, ' + start_time + ' I run for Save the Children. Please donate...';
    graph.put_wall_post(message=txt, attachment=attachment)

    return '0'

@app.route('/stop-training-action')
def stop_training_action():
    #print 'function called again'
    #print start_time
    client2=fitbit.Fitbit(consumer_key, client_secret, resource_owner_key = resource_owner_key, resource_owner_secret = resource_owner_secret)

    data = client2._COLLECTION_RESOURCE('activities')
    activities = data['activities']
    if len(activities) > 0:
	activity = activities[-1]
	#print activity
    else:
    	#print data
	activity = {}
	activity['distance'] = 1.2
	activity['duration'] = 1036
	activity['calories'] = 49

    graph = facebook.GraphAPI('CAAOFsL4kRvkBAG7s3VF29TX7iPZB2CzRZAn2BeIqZBaDtjBd6wtQFWe72YR8i51MSDfmAH0eX7FfBmSaGT1PiPw1Y7HJ4xtWMVhpNOoOh44Yy1TYeucQPQSS9GVTsC7UjpbRBK7Wd3fqZAQVVlHb6DKSal04eYqm0iJLWt3QtjXG0MEVQ80FdYzB9DRqAHzcJNR5O9hfZCzAkG0yFJDGt8pE7ZBsvoZBcAZD')
    profile = graph.get_object('me')
    
    msg = 'Today I ran ' + str(activity['distance']) + ' miles in ' + str(activity['duration'] / 1000) + ' seconds ' + ' and burnt ' + str(activity['calories']) + ' calories, to raise money for save the children, helping children in over 120 countries. Please donate if you can, no child is born to die. https://secure.savethechildren.org.uk/donate/';
    graph.put_object('me', 'feed', message=msg)

    return '0'
