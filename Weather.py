import re, sys
import urllib2
#from pyowm import OWM
from kdtree import KDTree

def get_country_from_user():
  print("Please a State for US stations or Country for international: ")
  sys.stdout.flush()
  cntry = raw_input("")
  return cntry.upper()
  
def get_stations():
  # get page with stations information including coordinates
  response = urllib2.urlopen('http://weather.rap.ucar.edu/surface/stations.txt')
  html = response.read()
  
  # Request Country from User
  cntry = get_country_from_user()
  print "The country selected was", cntry
  sys.stdout.flush()
  
  # find country
  Country_Index = re.search(cntry[0:-1].upper(), html).start()

  # only keep html after country, substring with 2 newlines consecutively
  html = html[Country_Index:]
  Country_METARs = html[:html.index("\n\n")]
  
  countries_stations = Country_METARs.split('\n')
  countries_stations.pop(0)

  return countries_stations
  
def stations_from_html_lines(countries_stations):
  METARs = []

  for METAR in countries_stations:
    METAR = " ".join(METAR.split())
    tmp3 = METAR.split(' ')
    j = 1
    while ((not tmp3[j].isupper()) or (not len(tmp3[j])==4) or ((not tmp3[j][0] == 'E') and (not tmp3[j][0] == 'O')) ):
      j+=1
    METARs.append(tmp3[j])
  
  return METARs

def write_stations_file(Num_Metars, METARs):
  print("was last here 3")
  Metar_print = open("Stations.txt","w")

  METAR_data = []
  coord_station_dict = {}
  
  i = 0
  while i < Num_Metars:
    response = urllib2.urlopen('http://weather.gladstonefamily.net/site/'+METARs[i])
    html = response.read()

    Lat_Line = html[html.index("Latitude"):html.index("Longitude")]
    Lon_Line = html[html.index("Longitude"):html.index("Elevation")]

    Metar_print.write(METARs[i])
    Metar_print.write(" "+ Lat_Line[Lat_Line.index("sec), ")+6:Lat_Line.index("&deg; (")]) 
    Metar_print.write(" "+Lon_Line[Lon_Line.index("sec), ")+6:Lon_Line.index("&deg; (")]+"\n")
    METAR_data.append((float(Lat_Line[Lat_Line.index("sec), ")+6:Lat_Line.index("&deg; (")]),float(Lon_Line[Lon_Line.index("sec), ")+6:Lon_Line.index("&deg; (")])))
    coord_station_dict[(float(Lat_Line[Lat_Line.index("sec), ")+6:Lat_Line.index("&deg; (")]),float(Lon_Line[Lon_Line.index("sec), ")+6:Lon_Line.index("&deg; (")]))] = METARs[i]
    i+=1
  
  return (METAR_data, coord_station_dict)

def get_weather_at_OWM(ref_point):
  """
    use openweather map to get weather at date and coordinates,
      unreliable and sparse outside of US in historical data,
      very accurate and high resolution points in US, should use this for US
  """
  owm_en = OWM("67f7b89fec64088749b0ecc406dda8bc") 

  obs = owm_en.weather_at_coords(-0.107331,51.503614)  
  #obs = owm_en.weather_history_at_coords(-0.107331,51.503614, '2013-09-13 16:46:40+00', '2013-09-13 19:16:40+00')
  print obs  

  w = obs.get_weather()

  print w.get_visibility_distance()
  print w.get_clouds()
  print w.get_snow()
  print w.get_rain()  
  print w.get_wind() 
  print w.get_humidity()  
  print w.get_pressure()  
  print w.get_temperature()   
  print w.get_detailed_status()  
  print w.get_sunset_time('iso')  
  
def query_nearest(METAR_data, ref_point):
  tree = KDTree.construct_from_data(METAR_data)

  nearest = tree.query(query_point=ref_point)
  
  return nearest
  
def main():
  countries_stations = get_stations()

  METARs = stations_from_html_lines(countries_stations)
  
  print METARs
  Num_Metars = len(METARs)

  METAR_data, coord_station_dict = write_stations_file(Num_Metars, METARs)
  
  reference_point = (35,70)
  nearest = query_nearest(METAR_data, reference_point)
  nearest_station = coord_station_dict[(nearest[0])]
  
  print nearest
  print coord_station_dict[(nearest[0])]
  
  
  #                   https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=OAJL&data=all&year1=1936&month1=1&day1=1&year2=2018&month2=4&day2=18&tz=Etc%2FUTC&format=onlycomma&latlon=no&direct=no&report_type=1&report_type=2
  history_data_url = 'https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=' + nearest_station + '&data=all&year1=1936&month1=1&day1=1&year2=2018&month2=4&day2=18&tz=Etc%2FUTC&format=onlycomma&latlon=no&direct=no&report_type=1&report_type=2'
  response = urllib2.urlopen(history_data_url)
  html = response.read()
  for line in html.split('\n'):
    print
    print
    print html.split(',')

if __name__ == '__main__':
  main()