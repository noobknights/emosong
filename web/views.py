from django.shortcuts import render
from django.contrib import messages
from json import dumps
import requests
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# Create your views here.
def index(request):
    test = os.getenv('ENV')
    print(test)
    return render(request, 'web/index.html', {'test':test})    