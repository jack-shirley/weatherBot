#Program used to get weather and text myself

import smtplib
import json
from pyowm.owm import OWM

def loader():
    with open("../res/data.json", "r") as file:
        setup = json.load(file)
    return setup

if __name__ == "__main__":
    setup_data = loader()

    KEY = setup_data['api_key']
    EMAIL = setup_data['email']
    PASSWORD = setup_data['password']
    LOCATION = setup_data['location']
    RECIPIENTS = setup_data['recipients']

    #valide api key w/ server
    owm = OWM(KEY)
    mgr = owm.weather_manager()
    weather = mgr.weather_at_place(LOCATION).weather

    temperature = weather.temperature(unit='fahrenheit')
    clouds = weather.detailed_status
    winds = weather.wnd

    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(EMAIL,PASSWORD)
    for recipient in RECIPIENTS:
        smtpObj.sendmail(EMAIL, recipient, 
        'Subject: Weather Report\n' +
        'It is currently ' + str(round(temperature['temp'])) + ' degrees in ' + LOCATION + '\n' +
        'with a high of ' +  str(round(temperature['temp_max'])) + 
        ' and a low of ' +  str(round(temperature['temp_min'])) + '\n\n' +
        'There is ' + clouds + ' and winds at ' + str(round(winds['speed'])) + 
        ' out of ' + str(winds['deg']) + '\n\n' +
        'Have a wonderful day.')