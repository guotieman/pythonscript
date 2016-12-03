# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event, vDatetime
from datetime import datetime

def get_arsenal_fixture_html():
    url = 'http://www.arsenal.com.cn/html/fixtures/2016-2017/'
    resp = requests.get(url)
    resp.encoding = 'gb2312'
    return resp.text

def parse_arsenal_fixture(html_text):
    arsenal_fixture = []
    soup = BeautifulSoup(html_text, "html.parser")
    year = ''
    month = ''
    day = ''
    time = ''
    p = re.compile(r'\d+')

    for tr in soup.find_all('tr'):
        if tr.th:
            if tr.th.text == u'热身赛':
                break
            year, month = p.findall(tr.th.text)
        tds = tr.find_all('td')
        if tds and not tds[6].text:
            day = tds[0].text
            desc = tds[2].text
            player = tds[4].text
            time = tds[5].text
            arsenal_fixture.append({
                    'datetime': '%s-%s-%s %s:00' % (year, month, day, time),
                    'summary': u'阿森纳VS' + player + '('+ tds[3].text +')',
                    'desc': desc
                })
    return arsenal_fixture

def __trans_calendar_time(datetime_str):
    start_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return vDatetime(start_time).to_ical()

def make_arsenal_fixture_calendar(arsenal_fixture):
    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//Eugene Liu'

    for fixture in arsenal_fixture:
        event = Event()
        event.add('summary', fixture['summary'])
        event['dtstart'] =  __trans_calendar_time(fixture['datetime'])
        event.add('description', fixture['desc'])
        cal.add_component(event)
    return cal.to_ical()

def main():
    html_text = get_arsenal_fixture_html()
    arsenal_fixture = parse_arsenal_fixture(html_text)
    arsenal_fixture_cal =  make_arsenal_fixture_calendar(arsenal_fixture)
    with open('/Users/eugene/workspace/iCalender/arsenal_fixture_cal.ics', 'wb') as f:
        f.write(arsenal_fixture_cal)
        f.close()
    print 'Success'

if __name__ == '__main__':
    main()
