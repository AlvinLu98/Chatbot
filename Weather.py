import pyowm

def get_weather(location):
    owm = pyowm.OWM('a7080f10eed08a6cc2a49b6564546bf3')
    location = location + ",GB"
    try:
        obs = owm.weather_at_place(location)
        w = obs.get_weather()
        return w
    except:
        return None

def get_temp(w):
    return w.get_temperature(unit='celsius')

def main():
    print(get_weather("Norwich"))

if __name__ == '__main__':
    main()