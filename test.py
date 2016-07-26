import json
import senml
from pprint import pprint

js = json.loads('''
[
{
    "bn":"urn:dev:mac:0b92569229fc9e68/rpm/",
    "bt":0,
    "bu":"1/min",
    "bver":5,
    "n":"fwd",
    "v":17.666544,
    "s":3,
    "t":0
},
{
    "n":"rev",
    "v":17.666544,
    "s":4,
    "t":0
}
]
''')

pprint(js)

s = senml.SenMLDocument.from_json(js)
pprint(s.measurements)

print("json:")
print("%r" % json.dumps(s.to_json(), sort_keys=True))
