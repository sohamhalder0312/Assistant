import pyttsx3
from datetime import datetime
import requests
import json
import streamlit as st
import qrcode
import string

def say(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice',voices[0].id)
        engine.setProperty('rate',190)
        engine.setProperty('volume',0.6)
        engine.say(text)
        engine.runAndWait()
    except:
        pass
st.title('Assistant')

def greeting():
    today = datetime.now()
    hour = today.hour
    minute = today.minute

    if hour<=12:
        real_hour = hour
    else:
        real_hour = hour - 12 
    if hour>=6 and hour<12:
        st.text(f'Good morning .')
        say(f'Good morning .')
        st.text(f'Current time is, {real_hour}:{minute} AM')
        say(f'Current time is, {real_hour}:{minute} AM')
    elif hour>=12 and hour<17:
        st.text(f'Good afternoon .')
        say(f'Good afternoon .')
        st.text(f'Current time is, {real_hour}:{minute} PM')
        say(f'Current time is, {real_hour}:{minute} PM')
    elif hour>=17 and hour<20:
        st.text(f'Good evening .')
        say(f'Good evening .')
        st.text(f'Current time is, {real_hour}:{minute} PM')
        say(f'Current time is, {real_hour}:{minute} PM')
    elif hour>=20:
        st.text(f'Good night .')
        say(f'Good night .')
        st.text(f'Current time is, {real_hour}:{minute} AM')
        say(f'Current time is, {real_hour}:{minute} AM')

ch = st.selectbox('What do you like to know?',['Greeting','QR Code','Jokes','Weather'])

if ch=='Greeting':
    greeting()
elif ch=='QR Code':
    st.header("Create QR")
    choise = st.selectbox("Please enter your choise",['Choose Type','Generate normal QR','Generate QR for UPI'])
    if choise=='Generate normal QR':
        st.header('Please fill up the details :')
        link = st.text_input('Enter your URL')
        if link=='':
            st.warning('Please enter a valid URL to generate QR code.')
            say('Please enter a valid URL to generate QR code.')
        else:
            st.info(f'Your URL is: {link}')    
            image = qrcode.make(link)
            if st.button('Create'):
                image.save('mycode.png')
                st.image('mycode.png', caption='Your QR', use_container_width=True)
                st.success('QR code created successfully!')
                say('QR code created successfully!')
    elif choise=='Generate QR for UPI': 
        st.header('Please fill up the details :')
        upi_id = st.text_input('What is your UPI ID? ')
        name = st.text_input('Please enter the payee name? ')
        new_name = name.replace(' ','%20')
        amount = st.text_input('Enter the amount: ')
        currency = st.text_input('Please enter the currency: (If currency is INR the skip this by pressing ENTER)')
        if currency=='':
            currency = 'INR'
        url = f"upi://pay?pa={upi_id}&pn={new_name}&am={amount}&cu={currency}"
        if upi_id=='' or name=='' or amount=='':
            st.warning('Please fill all the details to generate UPI QR code.')
            say('Please fill all the details to generate UPI QR code.')
        else:
            st.info(f'Your URL is: {url}')
            image = qrcode.make(url)
            if st.button('Create'):
                image.save('upiqr.png')
                st.image('upiqr.png', caption='Your UPI QR', use_container_width=True)
                st.success('UPI QR code created successfully!')
                say('UPI QR code created successfully!')

elif ch=='Jokes':
    st.header('Jokes')
    try:
        url = 'https://official-joke-api.appspot.com/random_joke'
        response = requests.get(url)
        data = response.json()
        st.text(data['setup'])
        say(data['setup'])
        st.text(data['punchline'])
        say(data['punchline'])
    except:
        st.warning('Oops...looks like something went wrong. Check the internet connection.')
        say('Oops...looks like something went wrong. Check the internet connection.')

elif ch=='Weather':
    st.header('Brief weather report')
    city=st.text_input('Please tell me the city name:')
    try:
        url = f'https://wttr.in/{city}?format=j1'
        st.info(url)
        if city=='':
            st.warning('Please enter a city name to get the weather report.')
            say('Please enter a city name to get the weather report.')
        else:
            response = requests.get(url)
            data = response.json()
            current = data['current_condition'][0]
            area = data['nearest_area'][0]
            astronomy = data['weather'][0]['astronomy'][0]
            # Extract specific values
            feels_like = current['FeelsLikeC']
            cloud_cover = current['cloudcover']
            visibility = current['visibility']
            humidity = current['humidity']
            pressure = current['pressureInches']
            temp = current['temp_C']
            popu = area['population']
            sunrise = astronomy['sunrise']
            sunset = astronomy['sunset']
            # Display Work
            st.header('WEATHER INFORMATION')
            st.text(f'City: {area['areaName'][0]['value']}')
            st.text(f"Temperature: {temp}*C (Feels Like: {feels_like}*C)")
            st.text(f"Cloud cover: {cloud_cover}%")
            st.text(f"Visibility: {visibility} km")
            st.text(f"Humidity: {humidity}%")
            st.text(f"Population: {popu}")
            st.text(f"Sunrise: {sunrise}")
            st.text(f"Sunset: {sunset}")
            st.text(f"Pressure: {pressure} inches")
    except:
        st.warning('Oops...looks like something went wrong. Check the internet connection.')

        say('Oops...looks like something went wrong. Check the internet connection.')
