import re
import urllib2
response = urllib2.urlopen('http://weather.rap.ucar.edu/surface/stations.txt')
html = response.read()

var = raw_input("Please enter something: ")
print "you entered", var

#print html

print html[:html.index("\n\n")]

Country_Index = re.search(var[0:-1].upper(), html).start()

html = html[Country_Index:]
Country_METARs = html[:html.index("\n\n")]

tmp2 = Country_METARs.split('\n')
tmp2.pop(0)

METARs = []

for a in tmp2:
	a = " ".join(a.split())
	tmp3 = a.split(' ')
	j = 1
	while ((not tmp3[j].isupper()) or (not len(tmp3[j])==4) or ((not tmp3[j][0] == 'E') and (not tmp3[j][0] == 'O')) ):
		print tmp3[j]
		j+=1
	print tmp3[j]
	METARs.append(tmp3[j])


print METARs
Num_Metars = len(METARs)

Metar_print = open("Stations.txt","w")

data = []

i = 0
while i < Num_Metars:
	response = urllib2.urlopen('http://weather.gladstonefamily.net/site/'+METARs[i])
	html = response.read()

	Lat_Line = html[html.index("Latitude"):html.index("Longitude")]
	Lon_Line = html[html.index("Longitude"):html.index("Elevation")]

	Metar_print.write(METARs[i])
	Metar_print.write(" "+ Lat_Line[Lat_Line.index("sec), ")+6:Lat_Line.index("&deg; (")]) 
	Metar_print.write(" "+Lon_Line[Lon_Line.index("sec), ")+6:Lon_Line.index("&deg; (")]+"\n")
	data.append((float(Lat_Line[Lat_Line.index("sec), ")+6:Lat_Line.index("&deg; (")]),float(Lon_Line[Lon_Line.index("sec), ")+6:Lon_Line.index("&deg; (")])))
	i+=1
	
from kdtree import KDTree

tree = KDTree.construct_from_data(data)

nearest = tree.query(query_point=(35,70))

print nearest