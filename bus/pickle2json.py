import pickle, json
dyct = pickle.loads(open('routedata', 'rb').read())
with open('routedata.json', 'w+') as file:
    file.write(json.dumps(dyct, indent=4))