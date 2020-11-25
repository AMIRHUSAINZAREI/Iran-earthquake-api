import re
import datetime
import requests
import unicodedata
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from .models import EarthQuake


def scraper():

    feildes = ['origin_time', 'magnitude', 'latitude', 'longitude', 'depth', 'region']

    # regex4extracting feildes 
    regex_patterns = ['.*?(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{1,2}).*',
                      '.*?(\d{1,2}\.\d{1}).*',
                      '.*?(\d{2}\.\d{3}).*',
                      '.*?(\d{2}\.\d{3}).*',
                      '.*?(\d{1,2}).*',
                      '.*?\>([\w\s]*\,  [\w\s]*).*?\<.*']

    # result dictionary
    earth_quakes = {}
    # handel result dictionary keys and count earthquakes
    earth_quake = 1

    # handel scraping 3 pages
    for i in range(1,4):
        response = requests.get('http://irsc.ut.ac.ir/index.php?page=%d'%i)
        content = response.content

        soup = BeautifulSoup(content, 'lxml')
        all_tr_tags = soup.find_all('tr')

        all_tr_tags_list = []
        for tr in all_tr_tags:
            if 'class' in tr.attrs:
                if 'DataRow1' in tr.attrs['class'][0] or 'DataRow2' in tr.attrs['class'][0]:
                    all_tr_tags_list.append(tr)

        for tr in all_tr_tags_list:
            earth_quakes[earth_quake] = {}
            tds = tr.find_all('td')
            for feilde in feildes:
                if feilde == 'origin_time':
                    _datetime = re.findall(r'%s'%regex_patterns[0], str(tds[0]))[0]
                    _datetime = datetime.datetime.strptime(_datetime, '%Y-%m-%d %H:%M:%S.%f')
                    earth_quakes[earth_quake]['origin_time']=_datetime
                elif feilde == 'magnitude':
                    earth_quakes[earth_quake]['magnitude']=float(re.findall(r'%s'%regex_patterns[1],
                                                                                    str(tds[1]))[0])
                elif feilde == 'latitude':
                    earth_quakes[earth_quake]['latitude']=float(re.findall(r'%s'%regex_patterns[2],
                                                                                   str(tds[2]))[0])
                elif feilde == 'longitude':
                    earth_quakes[earth_quake]['longitude']=float(re.findall(r'%s'%regex_patterns[3],
                                                                                    str(tds[3]))[0])
                elif feilde == 'depth':
                    earth_quakes[earth_quake]['depth']=float(re.findall(r'%s'%regex_patterns[4],
                                                                                str(tds[4]))[0])
                elif feilde == 'region':
                    raw_string = re.findall(r'%s'%regex_patterns[5],
                                                     str(tds[5]))[0]
                    # remove '\xa0' from beginning
                    new_string = unicodedata.normalize('NFKD', raw_string)
                    without_starter_space = re.sub(r'^\s+', '', new_string)
                    without_ender_space = re.sub(r'\s+$', '', without_starter_space)
                    earth_quakes[earth_quake]['region']=without_ender_space

            earth_quake = earth_quake + 1

    return earth_quakes


def update_earthquake_model():

    model_data = EarthQuake.objects.all()
    last_data = model_data[len(model_data)-1]
    last_data_date = last_data.origin_time

    # recent scraped data
    recent_earth_quake = scraper()

    # for over reversed earthquake
    for earth_quake in list(recent_earth_quake.items())[::-1]:
        if earth_quake[1]['origin_time'] > last_data_date:
            EarthQuake(origin_time=earth_quake[1]['origin_time'],
                       magnitude=earth_quake[1]['magnitude'],
                       latitude=earth_quake[1]['latitude'],
                       longitude=earth_quake[1]['longitude'],
                       depth=earth_quake[1]['depth'],
                       region=earth_quake[1]['region']).save()

def init_data():
    recent_earth_quake = scraper()
    for earth_quake in list(recent_earth_quake.items())[::-1]:
        EarthQuake(origin_time=recent_earth_quake[earth_quake[0]]['origin_time'],
                   magnitude=recent_earth_quake[earth_quake[0]]['magnitude'],
                   latitude=recent_earth_quake[earth_quake[0]]['latitude'],
                   longitude=recent_earth_quake[earth_quake[0]]['longitude'],
                   depth=recent_earth_quake[earth_quake[0]]['depth'],
                   region=recent_earth_quake[earth_quake[0]]['region']).save()

def sample_view(requests):
    update_earthquake_model()
    return HttpResponse('Done!')
