# eink-weatherforecast

Create an image suitable to be displayed on a SoluM ST-GR29000 ePaper price tag.
The image shows the current temperature and pressure, the general weather as a pictogram, the temperature forecast in one hour, the pressure forecast in one day, the date and time of the image creation and a graph of temperature and pressure forcast for the next 48 hours.
The weather data is gathered from OpenWeatherMap 
[OpenWeatherMap](https://openweathermap.org "https://openweathermap.org") 
using their OneCall-API v2.5

# Prerequisites

The python script currently uses Python 3.9.2 with PyYAML 6.0, Pillow 9.3.0, pyowm 3.3.0 and matplotlib 3.6.2
Especially if you run the scripts from cron, make sure the packages are installed in the system, not in the user path only.
Make sure you have the right version installed in the system paths, it is quite confusing if you test the scripts as a regular user and exhibit strange behaviour when run from cron due to different versions installed in the system and user path. Don't ask how I know...
To access OpenWeatherMap, you need to create a free account and generate an API key.

    sudo pip install pyowm Pillow matplotlib pyyaml

# The generated image

A generated image looks similar to the following example:

![weather display](https://github.com/dl6lr/eink-weatherforecast/blob/main/weather.jpg "weather display")

Description: 
Current temperature -0.1°C, no change expected for the next hour. 
Current pressure 1005hPa, rising to 1011hPa in the next 24 hours.
Current condition cloudy.
Graph for the next 48 hours, temperature in red, pressure in black.
Image created on December 9th, 2022 at 10:40:54

# Configuration

Configuration is done in config.yml that resides beneath owm.py. If you download the package for the first time, copy the sample file to config.yl and edit it.
Paste your OWM API key to config.yml and set your city and country:

    owm:
        api_key: 0123456789...abcdef
        location: Hamburg
        country: DE

See more configurable values in the configuration file.

Running the script with:

    python owm.py

should give no error message and the file weather.jpg should be updated.  The image fits the price tags orientation with the barcode to the left.

# Known bugs

The location query does not check for the result set. It expects at least one hit and uses the first one. If no hit is found, it fails with an exception:

    location = 'Gndfertyz'
    country = 'DE'

    Traceback (most recent call last):
      File "/home/pi/owm/owm.py", line 119, in <module>
        one_call = getOneCall(api_key, location, country)
      File "/home/pi/owm/owm.py", line 44, in getOneCall
        home = homelist[0]
    IndexError: list index out of range

Error handling is missing at other places too, so if anything fails do not expect the script to finish gracefully.
