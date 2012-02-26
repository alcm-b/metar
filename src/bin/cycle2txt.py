#!/usr/bin/python
import string
import fileinput
import re

timestamp_field = r"\d\d\d\d/\d\d/\d\d \d\d:\d\d"
metar_fields    = {
            'code'          : (r"^(\w{3,4})\b",                     lambda a: a)
           ,'temperature'   : (r"\b(M?\d\d)(?:/M?\d\d)\b",          lambda a: string.replace(a, 'M', '-'))
           ,'wind_direction': (r"(\d\d\d)(?:\d\d(G\d\d)?KT)\b",     lambda a: a)
# TODO knots, mph to meters per second
           ,'wind_speed'    : (r"(?<=\d\d\d)(\d\d)(?:G\d\d)?KT\b",  lambda a: a)
           ,'wind_gust'     : (r"(?<=\d\d\d\d\dG)(\d\d)(?:KT)\b",   lambda a: a)
# TODO handle 'time' as any other field
           ,'time'          : (r"^$",                               lambda a: "%s:00" % string.replace(a, '/', '-'))
        }
# TODO
metar_to_observation = [
            ( "temperature", )
        ]
observation_columns = [
            "idobservation"
           ,"station_idstation"
           ,"code"
           ,"time"
           ,"temperature"
           ,"wind_speed"
           ,"wind_direction"
        ]

# TODO get _idstation from .. somewhere
dummy_field_values = {"idobservation": '\N', "station_idstation": '7147'}
field_values = dummy_field_values

for line in fileinput.input():
    match = re.search(timestamp_field, line)
    if match is not None:
        timestamp = match.group(0)
        field_values['time'] = timestamp # "2011-01-21 10:10:10"
        continue

    if 'time' in field_values.keys():
        # timestamp field is read
        m = re.search(metar_fields['code'][0], line) 
        if m is None:
            continue
        for i in metar_fields:
            #if metar_fields[i][0] is not None :
            m = re.search(metar_fields[i][0], line) 
            if m is not None:
                field_values[i] = m.group(1)
            #   print "%s: %s" % (i, m.group(1))

# 1 pretty-printed values
#        print "--------------------------\n", line,
#        for i in observation_columns :
#            if field_values.get(i) :
#               print "%15s: %s" % (i, field_values[i]) 

# 2 tab-separated values
        list = []
        for i in observation_columns :
            if field_values.get(i) :
                value = field_values[i]
                if metar_fields.get(i) :
                    value = metar_fields[i][1](value)
                list.append(value)
        print "\t".join(list)

    field_values = dummy_field_values
