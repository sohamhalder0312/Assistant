from datetime import datetime
import requests
import streamlit as st
import qrcode
import io

st.title('SmartDesk - one place for your small everyday tools')

def greeting():
    today = datetime.now()
    hour = today.hour
    minute = today.minute
    if hour<=12:
        real_hour = hour
    else:
        real_hour = hour - 12
    
    if hour >= 6 and hour < 12:
        st.text('Good morning.')
        st.text(f'Current time is, {real_hour}:{minute:02d} AM')
    elif hour >= 12 and hour < 17:
        st.text('Good afternoon.')
        st.text(f'Current time is, {real_hour}:{minute:02d} PM')
    elif hour >= 17 and hour < 20:
        st.text('Good evening.')
        st.text(f'Current time is, {real_hour}:{minute:02d} PM')
    elif hour >= 20 or hour < 6:
        st.text('Good night.')
        # Shows AM for late night, adjust if preferred
        st.text(f'Current time is, {real_hour}:{minute:02d} AM')

ch = st.selectbox('What do you like to know?', ['Greeting', 'QR Code', 'Jokes', 'Weather'])

if ch == 'Greeting':
    greeting()

elif ch == 'QR Code':
    st.header("Create QR")
    choise = st.selectbox("Please enter your choice", ['Choose Type', 'Generate normal QR', 'Generate QR for UPI'])
    if choise == 'Generate normal QR':
        link = st.text_input('Enter your URL')
        if link == '':
            st.warning('Please enter a valid URL to generate QR code.')
        else:
            st.info(f'Your URL is: {link}')
            if st.button('Create'):
                qr_image = qrcode.make(link)
                buf = io.BytesIO()
                qr_image.save(buf, format="PNG")
                st.image(buf, caption='Your QR', use_container_width=True)
                st.success('QR code created successfully!')
    elif choise == 'Generate QR for UPI': 
        upi_id = st.text_input('What is your UPI ID? ')
        name = st.text_input('Please enter the payee name? ')
        amount = st.text_input('Enter the amount: ')
        currency = st.text_input('Currency (default: INR)')
        currency = currency if currency else 'INR'
        if upi_id and name and amount:
            new_name = name.replace(' ', '%20')
            url = f"upi://pay?pa={upi_id}&pn={new_name}&am={amount}&cu={currency}"
            st.info(f'Your URL is: {url}')
            if st.button('Create'):
                qr_image = qrcode.make(url)
                buf = io.BytesIO()
                qr_image.save(buf, format="PNG")
                st.image(buf, caption='Your UPI QR', use_container_width=True)
                st.success('UPI QR code created successfully!')
        else:
            st.warning('Please fill all the details to generate UPI QR code.')

elif ch == 'Jokes':
    st.header('Jokes')
    try:
        url = 'https://official-joke-api.appspot.com/random_joke'
        response = requests.get(url, timeout=10)
        data = response.json()
        st.text(data.get('setup', 'No joke found.'))
        st.text(data.get('punchline', ''))
    except Exception as e:
        st.warning(f'Oops...something went wrong. Check your internet connection. ({e})')

elif ch == 'Weather':
    st.header('Brief weather report')
    city = st.text_input('Please tell me the city name:')
    if city == '':
        st.warning('Please enter a city name to get the weather report.')
    else:
        try:
            url = f'https://wttr.in/{city}?format=j1'
            st.info(url)
            response = requests.get(url, timeout=10)
            data = response.json()
            current = data['current_condition'][0]
            area = data.get('nearest_area', [{}])[0]
            astronomy = data.get('weather', [{}])[0].get('astronomy', [{}])[0]
            feels_like = current.get('FeelsLikeC', '--')
            cloud_cover = current.get('cloudcover', '--')
            visibility = current.get('visibility', '--')
            humidity = current.get('humidity', '--')
            pressure = current.get('pressureInches', '--')
            temp = current.get('temp_C', '--')
            area_name = area.get('areaName', [{'value': '--'}])[0]['value']
            popu = area.get('population', '--')
            sunrise = astronomy.get('sunrise', '--')
            sunset = astronomy.get('sunset', '--')
            st.header('WEATHER INFORMATION')
            st.text(f'City: {area_name}')
            st.text(f"Temperature: {temp}°C (Feels Like: {feels_like}°C)")
            st.text(f"Cloud cover: {cloud_cover}%")
            st.text(f"Visibility: {visibility} km")
            st.text(f"Humidity: {humidity}%")
            st.text(f"Population: {popu}")
            st.text(f"Sunrise: {sunrise}")
            st.text(f"Sunset: {sunset}")
            st.text(f"Pressure: {pressure} inches")
        except Exception as e:
            st.warning(f'Oops...something went wrong. Check your internet connection. ({e})')


