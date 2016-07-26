"""SenML Python object representation"""

import attr

@attr.s
class SenMLMeasurement(object):
    """SenML data representation"""
    name = attr.ib(default=None)
    time = attr.ib(default=None)
    unit = attr.ib(default=None)
    value = attr.ib(default=None)
    base = attr.ib(default=None)
    sum = attr.ib(default=None)

    @classmethod
    def from_base_dict(cls, data):
        """Create a base instance from the given SenML data"""
        template = cls()
        attrs = {
            'name':  data.get('bn', template.name),
            'time':  data.get('bt', template.time),
            'unit':  data.get('bu', template.unit),
            'value': data.get('bv', template.value),
        }
        return cls(**attrs)

    @classmethod
    def from_json(cls, data, base=None):
        """Create an instance given JSON data as a dict"""
        if base is None:
            base = cls()

        attrs = {
            'name':  data.get('n', None),
            'time':  data.get('t', None),
            'unit':  data.get('u', None),
            'value': data.get('v', None),
            'sum': data.get('s', None),
            'base': base
        }
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

    def to_json(self, *, include_base=False):
        """Format the entry as a SenML+JSON object"""
        base = self.base if self.base is not None else self.__class__()
        ret = {}
        if include_base:
            # Add SenML version
            ret['bver'] = 5

            if base.name is not None:
                ret['bn'] = str(base.name)

            if base.time is not None:
                ret['bt'] = float(base.time)

            if base.unit is not None:
                ret['bu'] = str(base.unit)
            if base.value is not None:
                ret['bv'] = float(base.value)

        if self.name is not None:
            ret['n'] = str(self.name)

        if self.time is not None:
            ret['t'] = float(self.time)

        if self.unit is not None:
            ret['u'] = str(self.unit)

        if self.sum is not None:
            ret['s'] = float(self.sum)

        if isinstance(self.value, bool):
            ret['vb'] = self.value
        elif isinstance(self.value, bytes):
            ret['vd'] = self.value
        elif isinstance(self.value, str):
            ret['vs'] = self.value
        elif self.value is not None:
            ret['v'] = float(self.value)

        return ret

class SenMLDocument(object):
    """A collection of SenMLMeasurements"""

    measurement_factory = SenMLMeasurement

    def __init__(self, measurements=None, *args, **kwargs):
        """Constructor
        """
        super().__init__(*args, **kwargs)
        self.measurements = measurements

    @classmethod
    def from_json(cls, json_data):
        """Parse a loaded SenML JSON representation into a SenMLDocument

        @param[in] cls        this class
        @param[in] json_data  JSON list, from json.loads(senmltext)
        """
        # Grab base information from first entry
        base = cls.measurement_factory.from_base_dict(json_data[0])

        measurements = [cls.measurement_factory.from_json(item, base) for item in json_data]

        obj = cls(base=base, measurements=measurements)

        return obj

    def to_json(self):
        """Return a JSON dict"""
        if self.measurements:
            first = self.measurements[0].to_json(include_base=True)
            ret = [first]
            ret.extend([item.to_json() for item in self.measurements[1:]])
        else:
            ret = []
        return ret
