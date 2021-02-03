from django.shortcuts import render, redirect
from django.contrib import messages
from json import dumps
import requests
import os
import random
from pathlib import Path
from dotenv import load_dotenv
from model.face_detection import image
import urllib.parse

load_dotenv()

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
def index(request):
	return render(request, 'web/index.html')

def main(request):
	try:
		username = request.POST['username']
		imageData = request.POST['imagedata']
		if username != '':
			res = urllib.request.urlopen(imageData)
			with open('test.png', 'wb') as f:
				f.write(res.file.read())
			imagePath = str(BASE_DIR)+'/test.png'
			emotion = image(imagePath)
			print(emotion)
			emotionDict = ['angry','disgust','fear','happy','sad','surprise','relax']
			colors = ['blue', 'indigo','purple','pink','red','orange','yellow','green','teal','gray']
			if emotion == -1:
				return render(request, index(request), {'error':'Error Detecting Your Face'})
			else:
				emotion = emotionDict[emotion]
				song = getsong(emotion)
				color = random.choice(colors)
				return render(request, 'web/main.html', {'emotion':emotion, 'username':username, 'song':dumps(song), 'env':os.getenv('APP_ENV'), 'chathost':os.getenv('SOCKET_HOST'), 'color':color})

		return redirect('/')

	except:
		return render(request, 'web/index.html', {'error':'Server Error, Try again later!!!'})

# 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Relax

def getsong(category):
	songDict={'angry':'mood','disgust':'rnb','fear':'rock','happy':'wellness','sad':'anime','surprise':'edm_dance','relax':'chill'}
	category = songDict[category]
	url = "https://api.spotify.com/v1/browse/categories/"+str(category)+"/playlists"
	bearerToken = " ".join(["Bearer",os.getenv('SPOTIFY_TOKEN')])
	headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": bearerToken}
	response = requests.request("GET", url, headers=headers, data={})
	return response.json()


# worker: gunicorn -k uvicorn.workers.UvicornWorker emosong.asgi
