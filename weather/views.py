from django.shortcuts import render
import json
import urllib.request
import urllib.parse

def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        if city:  # Ensure city is not empty
            try:
                # Encode city to handle spaces and special characters
                city_encoded = urllib.parse.quote(city)
                api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_encoded}&appid=cb771e45ac79a4e8e2205c0ce66ff633'
                with urllib.request.urlopen(api_url) as response:
                    res = response.read()
                json_data = json.loads(res)
                data = {
                    "country_code": str(json_data['sys']['country']),
                    "coordinate": f"{json_data['coord']['lon']} {json_data['coord']['lat']}",
                    "temp": f"{json_data['main']['temp']}K",
                    "pressure": str(json_data['main']['pressure']),
                    "humidity": str(json_data['main']['humidity']),
                }
            except urllib.error.HTTPError as e:
                data = {'error': f'HTTP Error: {e.reason}'}
            except urllib.error.URLError as e:
                data = {'error': 'Could not retrieve data. Please check the city name or try again later.'}
                print(f"Error fetching data: {e}")
            except json.JSONDecodeError:
                data = {'error': 'Error decoding the response from the weather service.'}
            except KeyError:
                data = {'error': 'Unexpected response format from the weather service.'}
        else:
            data = {'error': 'City name cannot be empty.'}
    else:
        city = ''
        data = {}

    return render(request, 'index.html', {'city': city, 'data': data})
