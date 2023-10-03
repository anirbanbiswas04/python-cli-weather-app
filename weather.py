import argparse  # Easily make user friendly CLI also defines arguments which program can accept and show help text
import pyfiglet  # Create ASCII art from normal text
import requests  # Call API requests and show response
from halo import Halo  # Show loading
from simple_chalk import chalk  # Add color to text
import os
from dotenv import find_dotenv, load_dotenv


def main():
    # Initiate loading text and icon
    spinner = Halo(text='Loading', spinner='dots')

    # API key for openweathermap
    dot_env_path = find_dotenv()
    load_dotenv(dot_env_path)
    API_KEY = os.getenv('API_KEY')

    # Base weather for openweathermap API
    BASE_URL = f'http://api.openweathermap.org/data/2.5/weather'

    # Map the weather codes to weather icons
    WEATHER_ICONS = {
        # day icons
        '01d': '☀️',
        '02d': '⛅',
        '03d': '☁️',
        '04d': '☁️',
        '09d': '🌧️',
        '10d': '🌦️',
        '11d': '⛈️',
        '13d': '❄️',
        '50d': '🌫️',
        # night icons
        '01n': '🌛',
        '02n': '☁️',
        '03n': '☁️',
        '04n': '☁️',
        '09n': '🌧️',
        '10n': '🌦️',
        '11n': '⛈️',
        '13n': '❄️',
        '50n': '🌫️',
    }

    # Construct API URL with query parameters
    parser = argparse.ArgumentParser(description='Check the weather for a country or a city')
    parser.add_argument('country', help='The country or city to check the weather for')
    args = parser.parse_args()
    url = f'{BASE_URL}?q={args.country}&appid={API_KEY}&units=metric'

    # Show loading text and icon
    spinner.start()

    # Make API request and parse response using requests module
    response = requests.get(url)
    if response.status_code != 200:
        # Stop loading text and icon
        spinner.stop()
        # Show error message
        print(chalk.red("Error: Unable to retrive weather information"))
        exit()

    # Parsing the JSON response from the API and extract the weather information
    data = response.json()

    # Get information from response
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']
    icon = data['weather'][0]['icon']
    city = data['name']
    country = data['sys']['country']

    # Construct the output with weather icon
    weather_icon = WEATHER_ICONS.get(icon, '🌼')
    output = f"{pyfiglet.figlet_format(city)} {country}\n\n"
    output += f"{weather_icon}  {description}\n"
    output += f"Temperature: {temperature} °C\n"
    output += f"Feels like: {feels_like} °C\n"
    output += f"Humidity: {humidity}%"

    # Stop loading text and icon
    spinner.stop()

    # Print the output
    color = chalk.redBright if feels_like > 30 else (chalk.green if feels_like > 10 else chalk.blueBright)
    print(color.bold.underline(output))


if __name__ == '__main__':
    main()
