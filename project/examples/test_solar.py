def calculate_power(sunlight):
    return sunlight * 0.2

def process_data(data):
    result = fetch_sensor()
    clean = transform(result)
    store = save_to_db(clean)
    return store

def fetch_sensor():
    return get_raw_value()

def get_raw_value():
    return read_sensor()

def read_sensor():
    return 100

def transform(value):
    return value * 1.5

def save_to_db(value):
    global sensor_cache
    sensor_cache = value
    return value