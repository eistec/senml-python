"""@package senml.senml
SenML Python object representation

@todo Add CBOR support
"""

import attr
try:
    import cbor
except ImportError:
    HAVE_CBOR = False
else:
    HAVE_CBOR = True

@attr.s
class SenMLMeasurement(object):
    """SenML data representation"""
    name = attr.ib(default=None)
    time = attr.ib(default=None)
    unit = attr.ib(default=None)
    value = attr.ib(default=None)
    sum = attr.ib(default=None)

    def to_absolute(self, base):
        """Convert values to include the base information

        Be aware that it is not possible to compute time average of the signal
        without the base object since the base time and base value are still
        needed for that use case."""
        attrs = {
            'name': (base.name or '') + (self.name or ''),
            'time': (base.time or 0) + (self.time or 0),
            'unit': self.unit or base.unit,
            'sum':  self.sum,
        }
        if  isinstance(self.value, bool) or \
            isinstance(self.value, bytes) or \
            isinstance(self.value, str):
            attrs['value'] = self.value
        elif self.value is not None:
            attrs['value'] = (base.value or 0) + (self.value or 0)

        ret = self.__class__(**attrs)
        return ret

    @classmethod
    def base_from_json(cls, data):
        """Create a base instance from the given SenML data"""
        template = cls()
        attrs = {
            'name':  data.get('bn', template.name),
            'time':  data.get('bt', template.time),
            'unit':  data.get('bu', template.unit),
            'value': data.get('bv', template.value),
        }
        # Convert to numeric types
        cls.clean_attrs(attrs)

        return cls(**attrs)

    @staticmethod
    def numeric(val):
        """Convert val to int if the value does not have any decimals, else convert to float"""
        if val is None or isinstance(val, float) or isinstance(val, int):
            return val
        if float(val) == int(val):
            return int(val)
        else:
            return float(val)

    @classmethod
    def clean_attrs(cls, attrs):
        """Clean broken SenML+JSON with strings where there are supposed to be numbers"""
        # This fixes common typing errors such as:
        # [{"bn":"asdf","bt":"1491918634"}]
        # (where the value for bt: is supposed to be a numeric type, not a string)
        for key in ('time', 'sum', 'value'):
            val = attrs.get(key, None)
            attrs[key] = cls.numeric(val)

    @classmethod
    def from_json(cls, data):
        """Create an instance given JSON data as a dict"""
        template = cls()
        attrs = {
            'name':  data.get('n', template.name),
            'time':  data.get('t', template.time),
            'unit':  data.get('u', template.unit),
            'value': data.get('v', template.value),
            'sum':   data.get('s', template.sum),
        }
        # Convert to numeric types
        cls.clean_attrs(attrs)

        if attrs['value'] is None:
            if 'vs' in data:
                attrs['value'] = str(data['vs'])
            elif 'vb' in data:
                if str(data['vb']).casefold() == 'false'.casefold() or \
                    str(data['vb']).casefold() == '0'.casefold():
                    attrs['value'] = False
                else:
                    attrs['value'] = True
            elif 'vd' in data:
                attrs['value'] = bytes(data['vd'])


        return cls(**attrs)

    def to_json(self):
        """Format the entry as a SenML+JSON object"""
        ret = {}
        if self.name is not None:
            ret['n'] = str(self.name)

        if self.time is not None:
            ret['t'] = self.numeric(self.time)

        if self.unit is not None:
            ret['u'] = str(self.unit)

        if self.sum is not None:
            ret['s'] = self.numeric(self.sum)

        if isinstance(self.value, bool):
            ret['vb'] = self.value
        elif isinstance(self.value, bytes):
            ret['vd'] = self.value
        elif isinstance(self.value, str):
            ret['vs'] = self.value
        elif self.value is not None:
            ret['v'] = self.numeric(self.value)

        return ret

class SenMLDocument(object):
    """A collection of SenMLMeasurement data points"""

    measurement_factory = SenMLMeasurement

    def __init__(self, measurements=None, *args, base=None, **kwargs):
        """Constructor
        """
        super().__init__(*args, **kwargs)
        self.measurements = measurements
        self.base = base

    @classmethod
    def from_json(cls, json_data):
        """Parse a loaded SenML JSON representation into a SenMLDocument

        @param[in] json_data  JSON list, from json.loads(senmltext)
        """
        # Grab base information from first entry
        base = cls.measurement_factory.base_from_json(json_data[0])

        measurements = [cls.measurement_factory.from_json(item) for item in json_data]

        obj = cls(base=base, measurements=measurements)

        return obj

    def to_json(self):
        """Return a JSON dict"""
        first = {
            # Add SenML version
            'bver': 5,
        }
        if self.base:
            base = self.base
            if base.name is not None:
                first['bn'] = str(base.name)
            if base.time is not None:
                first['bt'] = float(base.time)
            if base.unit is not None:
                first['bu'] = str(base.unit)
            if base.value is not None:
                first['bv'] = float(base.value)

        if self.measurements:
            first.update(self.measurements[0].to_json())
            ret = [first]
            ret.extend([item.to_json() for item in self.measurements[1:]])
        else:
            ret = []
        return ret
