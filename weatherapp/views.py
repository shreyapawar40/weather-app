"""from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
   
    if 'city' in request.POST:
         city = request.POST['city']
    else:
         city = 'indore'     
    
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=95c9c6eab7ea5475d073649ff78be209'
    PARAMS = {'units':'metric'}

    API_KEY =  'AIzaSyAYBBQOnPSEqC_5581muyoInT6CWVQRUi8'

    SEARCH_ENGINE_ID = '26cd83dd9c4724988'
     
    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    count = 1
    search_items = data.get("items")
    image_url = search_items[1]['link']
    

    try:
          
          data = requests.get(url,params=PARAMS).json()
          description = data['weather'][0]['description']
          icon = data['weather'][0]['icon']
          temp = data['main']['temp']
          day = datetime.date.today()

          return render(request,'weatherapp/index.html' , {'description':description , 'icon':icon ,'temp':temp , 'day':day , 'city':city , 'exception_occurred':False ,'image_url':image_url})
    
    except KeyError:
          exception_occurred = True
          messages.error(request,'Entered data is not available to API')   
          # city = 'indore'
          # data = requests.get(url,params=PARAMS).json()
          
          # description = data['weather'][0]['description']
          # icon = data['weather'][0]['icon']
          # temp = data['main']['temp']
          day = datetime.date.today()

          return render(request,'weatherapp/index.html' ,{'description':'clear sky', 'icon':'01d'  ,'temp':25 , 'day':day , 'city':'indore' , 'exception_occurred':exception_occurred } )
               
    
    """

from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    city = request.POST.get('city') or 'indore'

    # OpenWeatherMap API
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b8012ffb9f9d1719db4db8bb10600674'
    PARAMS = {'units': 'metric'}

    # Google Custom Search API for image
    API_KEY = 'AIzaSyAYBBQ0nPSEqC_5581muyoInT6CWVQRUi8'
    SEARCH_ENGINE_ID = '26cd83dd9c4724988'
    query = city + " 1920x1080"
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start=1&searchType=image&imgSize=xlarge"

    image_url = ""
    day = datetime.date.today()

    try:
        # Image fetching
        img_data = requests.get(city_url).json()
        search_items = img_data.get("items", [])

        if isinstance(search_items, list) and len(search_items) >= 2:
            image_url = search_items[1]['link']
        elif isinstance(search_items, list) and len(search_items) == 1:
            image_url = search_items[0]['link']
        else:
            image_url = 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'

        # Weather fetching
        weather_data = requests.get(weather_url, PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'city': city,
            'day': day,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception as e:
        print(f"Error: {e}")
        messages.error(request, 'Entered data is not available to API')
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'city': 'indore',
            'day': day,
            'exception_occurred': True,
            'image_url': image_url
        })
