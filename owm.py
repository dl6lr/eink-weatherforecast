#
# SoluM-OWM
# 
# Requests weather information from OWM Open Weather Map
# and creates an image suitable to be placed on a SoluM ST-GR29000 e-paper tag
#
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import time
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import io
from datetime import datetime, tzinfo

# configuration section
#
# OWM API key
api_key = '<your-api-key>'

# Location and country to be used for the queries
location = '<your-city>'
country = 'DE'

# Filename used for the generated image
fname = 'weather.png'

# Big font for the temperature
bigfont = 'fonts/VeraSe18.pil'

# Small font for the pressure
smallfont = 'fonts/VeraSe12.pil'

# global owm configuration
config_dict = get_default_config()
config_dict['language'] = 'en'  # your language here

#
# getOneCall: requests current weather and forecasts in one call
#
def getOneCall(api_key, location, country):
  '''
  requests current weather and forecasts in one call

    Parameters:
    api_key: the OWM API key
    location: location to be looked up
    country: country of the location

    Returns: OWM onecall data structure
  '''
  owm = OWM(api_key, config_dict)

  geo = owm.geocoding_manager()
  homelist = geo.geocode(location, country = country)
  home = homelist[0]

  mgr = owm.weather_manager()

  one_call = mgr.one_call(home.lat, home.lon)
  return one_call

#
# arrayTempTendency: get array of temperature tendency
#
def arrayTempTendency(forecast):
  '''
    get array of temperature tendency

      Parameters:
        forecast: array with weather forecasts
  '''
  arr = []

  for weather in forecast:
    temp = round(weather.temperature('celsius')['temp'], 1)
#    hour = datetime.fromtimestamp(weather.reference_time(), tz=None).strftime("%H")
    arr.append(temp)
  return arr

#
# arrayPressTendency: get array of pressure tendency
#
def arrayPressTendency(forecast):
  arr = []

  for weather in forecast:
    press = weather.barometric_pressure()['press']
#    hour = datetime.fromtimestamp(weather.reference_time(), tz=None).strftime("%H")
    arr.append(press)
  return arr

#
# imageTendency: get tendency graph of temperature and pressure
#
def imageTendency(forecast):
  '''
    get tendency graph of temperature and pressure

      Parameters:
        forecast: array with weather forecasts

      Returns:
        image buffer in PNG format
  '''
  # In reality we have something more like 113dpi, but then the axis description is too large
  # Arrange with dpi and figsize to have about 225x108 pixel image area
  dpi = 90

  fig, ax1 = plt.subplots(figsize=(225/dpi, 108/dpi), dpi=dpi, facecolor=(1, 1, 1, 0))

  color = 'tab:red'
  ax1.plot(arrayTempTendency(forecast), color=color)
  ax1.tick_params(axis='y', labelcolor=color)
  ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

  color = '0'
  ax2.plot(arrayPressTendency(forecast), color=color)
  ax2.tick_params(axis='y', labelcolor=color)

  fig.tight_layout()  # otherwise the right y-label is slightly clipped

  img_buf = io.BytesIO()
  plt.savefig(img_buf, format='png')
  plt.clf()
  return img_buf

#
# ImageWeather: creates an image from the current weather, next hour and tomorrows weather forecasts
#
def ImageWeather(weather, onehour, tomorrow, tendency):
  '''
    creates an image from the current weather, next hour and tomorrows weather forecasts

      Parameters:
        weather: current weather data
        onehour: onehour forecast weather data
        tomorrow: tomorrow weather forecast

      Returns: 
        PIL Image object
  '''
  Black = (0, 0, 0)
  White = (255, 255, 255)
  Yellow = (255,255,127)

  time_string = time.strftime("%d.%m.%Y\n%H:%M:%S", time.localtime())

  image=Image.new("RGBA",(296,128),color=White)
  draw = ImageDraw.Draw(image)

  font = ImageFont.load(bigfont)
  temp1 = round(weather.temperature('celsius')['temp'], 1)
  temp2 = round(onehour.temperature('celsius')['temp'], 1)
  output=str(temp1) + '??C'
  draw.text((10, 0),output ,align='center',index=1,fill=Black,font=font)
  image.alpha_composite(Image.open('./icons/tendency/'+getTendency(temp1, temp2)+'.png'), dest=(90,5))
  output=str(temp2) + '??C'
  draw.text((120, 0),output ,align='center',index=1,fill=Black,font=font)

  font = ImageFont.load(smallfont)
  press1 = weather.barometric_pressure()['press']
  press2 = tomorrow.barometric_pressure()['press']
  output=str(press1) + 'hPa'
  draw.text((10, 30),output ,align='center',index=1,fill=Black,font=font)
  image.alpha_composite(Image.open('./icons/tendency/'+getTendency(press1, press2)+'.png'), dest=(90,27))
  output=str(press2) + 'hPa'
  draw.text((120, 30),output ,align='center',index=1,fill=Black,font=font)

  image.alpha_composite(Image.open('./icons/'+weather.weather_icon_name+'@2x.png'), dest=(196,0))

  font = ImageFont.load_default()
  draw.text((230, 100),time_string,index=1,fill=(0, 0, 0),font=font)

  # temp tendency
  img_buf = imageTendency(one_call.forecast_hourly)
  im = Image.open(img_buf)
  image.alpha_composite(im, dest=(0, 35))
  img_buf.close()

  image=image.rotate(90,expand=True)
  image.save(fname)
  return image

#
# getTendency: Returns a tendency string from two values.
#
def getTendency(val1, val2):
  '''
    Returns a tendency string from two values.

      Parameters:
        val1: first value
        val2: second value

	  Returns: 
        "up" if second value is greater than first value, "down" if second value is smaller than first value, "equal" if both are equal
  '''
  if val1 > val2:
    return 'down'
  elif val2 > val1:
    return 'up'
  else:
    return 'equal'

# main program

one_call = getOneCall(api_key, location, country)
image = ImageWeather(one_call.current, one_call.forecast_hourly[1], one_call.forecast_daily[1], one_call.forecast_hourly)

