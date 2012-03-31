#!/usr/bin/python
import sys
import string
import fileinput
import re

# :map <F3> :!tail -`perl -e "print int(15+rand(333)*15)"` ./scratch/00Z.TXT \| head -15 \| %<CR> 

def windspeed2mps(speed, unit) :
    rate = {'KT': 0.514444444, 'MPS': 1}
    if rate.get(unit) is not None:
        mps =  int(speed) * rate[unit]
    else :
        raise Exception("Unknown units of speed: %s" % unit)
    return "%.1f" % round(mps, 1)

timestamp_field = r"\d\d\d\d/\d\d/\d\d \d\d:\d\d"
metar_parsers    = {
            'code'          : (r"^(\w{3,4})\b",                             lambda t: t[0])
           ,'temperature'   : (r"\b(M?\d\d)(?:/M?\d\d)\b",                  lambda t: string.replace(t[0], 'M', '-'))
           ,'wind_direction': (r"(\d\d\d|VRB)(?:\d\d(G\d\d)?(MPS|KT))\b",   lambda t: string.replace(t[0], 'VRB', '\N'))
           ,'wind_speed'    : (r"(?<=\d\d\d|VRB)(\d\d)(?:G\d\d)?(MPS|KT)\b",lambda t: windspeed2mps(*t))
           ,'wind_gust'     : (r"(?<=\w\w\w\d\dG)(\d\d)(MPS|KT)\b",         lambda t: windspeed2mps(*t))
# TODO handle 'time' as any other field ?
           ,'time'          : (r"^$",                                       lambda t: "%s:00" % string.replace(t[0], '/', '-'))
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

default_values = {
            "idobservation": ('\N',)
# TODO get _idstation from .. somewhere
           ,"station_idstation": ('7147',)
           ,'temperature'   : ('\N',)
           ,'wind_direction': ('\N',)
           ,'wind_speed'    : ('\N',)
           ,'wind_gust'     : ('\N',)
       }

def decode(line, my_default_values):
    """Decodes a METAR report string using metar_parsers dict.

    >>> metar.decode("KFDW 242355Z AUTO -RA SCT080 17/12 ", {'time': '2012-02-25 00:37:00'})
    {'code': ('KFDW',), 'temperature': ('17',), 'time': '2012-02-25 00:37:00'}

    >>> metar.decode("KFDW 242355Z AUTO 24009G18KT 10SM -RA SCT080 17/12 A2974 RMK AO1", {'time': '2012-02-25 00:37:00'})
    {'wind_speed': ('09', 'KT'), 'code': ('KFDW',), 'temperature': ('17',), 'wind_direction': ('240', 'G18', 'KT'), 'time': '2012-02-25 00:37:00', 'wind_gust': ('18', 'KT')}
    """

    m = re.search(metar_parsers['code'][0], line) 
    if m is None:
        sys.stderr.write("Cannot parse METAR report " % line);
        # TODO raise exception
        return

    for i in metar_parsers:
        #if metar_parsers[i][0] is not None :
        m = re.search(metar_parsers[i][0], line) 
        if m is not None:
            my_default_values[i] = m.groups()
        #   print "%s: %s" % (i, m.group(1))
# 1 pretty-printed values
#        print "--------------------------\n", line,
#        for i in observation_columns :
#            if field_values.get(i) :
#               print "%15s: %s" % (i, field_values[i]) 
    return my_default_values

def dump_line(values, columns):
    """ Writes a tab-separated list of values containing the given list of column names
    """
    list = []
    for i in columns :
        if values.get(i) :
            value = values[i][0]
            if value <> '\N' and metar_parsers.get(i) :
                value = metar_parsers[i][1](values[i])
            list.append(value)
    return "\t".join(list)

if __name__ == '__main__':

    field_values = default_values.copy()
    for line in fileinput.input():
        # 1 skip empty lines
        if len(line) <= 1 : continue

        # 2 find a line with timestamp, save it for next iteration
        match = re.match(timestamp_field, line)
        if match is not None:
            timestamp = match.group(0)
            field_values['time'] = (timestamp,)
            continue

        # if there was a timestamp in previous line, process a METAR report
        if 'time' in field_values.keys():
            field_values = decode(line,field_values)
            if None == field_values: continue
            # 3 tab-separated values
            print dump_line(field_values, observation_columns)
            # 4 cleanup
            field_values = default_values.copy()
