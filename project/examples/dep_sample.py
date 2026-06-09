def fetch():
    return get_from_db()

def get_from_db():
    return {'data': 1}

def process():
    data = fetch()
    return data