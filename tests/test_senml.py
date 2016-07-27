"""Unit tests for senml.senml"""

import json
#import pytest

from senml import senml

JS = json.loads('''
[
{
    "bn":"urn:dev:mac:0b92569229fc9e68/rpm/",
    "bt":1234567890.123,
    "bu":"1/min",
    "bver":5,
    "n":"fwd",
    "v":17.666544,
    "s":3,
    "t":5
},
{
    "n":"rev",
    "v":123.456,
    "s":4,
    "t":7
},
{
    "n":"bool",
    "vb":true,
    "t":1
},
{
    "n":"str",
    "vs":"hej",
    "t":2
}
]
''')

FLOAT_TOLERANCE = 1e-7

def float_almost_equal(left, right):
    """Compare floats for almost equal"""
    return abs(left - right) < FLOAT_TOLERANCE

def test_senmldocument_from_json():
    """test SenMLDocument.from_json"""
    doc = senml.SenMLDocument.from_json(JS)
    assert isinstance(doc, senml.SenMLDocument)
    assert doc.base.name == 'urn:dev:mac:0b92569229fc9e68/rpm/'
    assert doc.base.unit == '1/min'
    assert doc.base.sum is None
    assert doc.base.value is None
    assert float_almost_equal(doc.base.time, 1234567890.123)

def test_senmlmeasurement_from_json():
    """SenMLMeasurement.from_json"""
    meas = senml.SenMLMeasurement.from_json(JS[0])
    assert isinstance(meas, senml.SenMLMeasurement)
    assert meas.name == 'fwd'
    assert float_almost_equal(meas.value, 17.666544)
    assert float_almost_equal(meas.sum, 3)
    assert float_almost_equal(meas.time, 5)

def test_senmlmeasurement_to_json():
    """test SenMLMeasurement.to_json"""
    meas = senml.SenMLMeasurement.from_json(JS[1])
    js_out = meas.to_json()
    assert js_out == JS[1]

def test_senmldocument_to_json():
    """test SenMLDocument.to_json"""
    doc = senml.SenMLDocument.from_json(JS)
    js_out = doc.to_json()
    assert js_out == JS

def test_senmlmeas_to_absolute():
    """test SenMLMeasurement.to_json"""
    doc = senml.SenMLDocument.from_json(JS)
    meas = senml.SenMLMeasurement.from_json(JS[1])
    mabs = meas.to_absolute(base=doc.base)
    assert isinstance(mabs, senml.SenMLMeasurement)
    assert mabs.name == 'urn:dev:mac:0b92569229fc9e68/rpm/rev'
    assert float_almost_equal(mabs.value, 123.456)
    assert float_almost_equal(mabs.sum, 4)
    assert float_almost_equal(mabs.time, 1234567897.123)
