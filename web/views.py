from django.shortcuts import render, redirect
from django.contrib import messages
from json import dumps
import requests
import os
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
	test = os.getenv('ENV')
	return render(request, 'web/index.html', {'test':test})

def main(request):
	username = request.POST['username']
	imageData = request.POST['imagedata']
	if username != '':
		res = urllib.request.urlopen(imageData)
		with open('test.png', 'wb') as f:
			f.write(res.file.read())
		imagePath = str(BASE_DIR)+'/test.png'
		print(imagePath)
		emotion = image(imagePath)
		print(emotion)
		emotionDict = ['angry','disgust','fear','happy','sad','surprise','relax']

		if emotion == -1:
			return redirect('/')
		else:
			emotion = emotionDict[emotion]
			song = getsong(emotion)
			return render(request, 'web/main.html', {'emotion':emotion, 'username':username, 'song':dumps(song)})

	return redirect('/')
# 0=Angry, 1=Disgust, 2=Fear, 3=Happy, 4=Sad, 5=Surprise, 6=Relax
# {angry:'hardstyle',disgust:'heavy-metal',fear:'soul',happy:'acoustic',sad:'groove',surprise:'anime',relax:'afrobeat'}

def getsong(category):
	songDict={'angry':'hardstyle','disgust':'heavy-metal','fear':'soul','happy':'acoustic','sad':'groove','surprise':'edm','relax':'afrobeat'}
	category = songDict[category]
	category = 'party'
	url = "https://api.spotify.com/v1/browse/categories/"+str(category)+"/playlists"
	headers = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Bearer "+str(os.getenv('TOKEN'))}
	response = requests.request("GET", url, headers=headers, data={})
	return response.json()