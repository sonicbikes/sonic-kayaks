import csv
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import json
import gmplot

def heatmap_colour(value):
    colours = [[0,0,1], [0,1,0], [1,1,0], [1,0,0]]
    idx1=0 
    idx2=0
    fract = 0
    if value<=0:  
        idx1 = idx2 = 0;            
    elif value>=1:  
        idx1 = idx2 = len(colours)-1; 
    else:
        value = value*(len(colours)-1); 
        idx1  = int(math.floor(value))        
        idx2  = int(idx1+1)  
        fract = value - float(idx1) 
    return [(colours[idx2][0] - colours[idx1][0])*fract + colours[idx1][0],
            (colours[idx2][1] - colours[idx1][1])*fract + colours[idx1][1],
            (colours[idx2][2] - colours[idx1][2])*fract + colours[idx1][2]]


gps = {}

#base_path = "archive/27072016-flushing/"
# 16.062 to 16.437
#base_path = "archive/24082016-penryn/"
# 17.625 to 18.062
base_path = "archive/06092016-swansea/2/"
#base_path = "archive/08012017-penryn/"
#base_path = "archive/220317-penryn/"
#base_path = "archive/25032017-penryn/2/"

gpsraw = open('gpsraw.txt','w')

gpsraw.write("latitude,longitude\n")

gps_centre = [0,0]
gps_count = 0
with open(base_path+'gps.log', 'r') as lines:
    for i,l in enumerate(lines):
        row = l.split()
        #print(row)
        if len(row)==7:
            #gpsraw.write(row[5]+", "+row[6]) 
            lon = float(row[5])
            lat = float(row[6])
            gps[row[3]]=[i,(lon,lat)]
            gps_centre[0]+=lon
            gps_centre[1]+=lat
            gps_count += 1

gps_centre[0]/=float(gps_count)
gps_centre[1]/=float(gps_count)

temp = []
with open(base_path+'temp.log', 'r') as lines:
    for l in lines:
        row = l.split(" ")
        #print row
        if len(row)==3:
            t = float(row[2])
            #print t
            if t<28.1 and row[1] in gps:
                pos = gps[row[1]]
                temp.append([pos,t])
            if row[0] in gps:
                pos = gps[row[1]]
                gpsraw.write(str(pos[1][0])+", "+str(pos[1][1])+"\n") 

gpsraw.close()

#exit()

min_temp = 9999
max_temp = 0

for t in temp:
    if t[1]<min_temp: min_temp=t[1]
    if t[1]>max_temp: max_temp=t[1]


min_temp = 17.687
#max_temp = 25.687
max_temp = 19.437

print ("min temp: "+str(min_temp))
print ("max temp: "+str(max_temp))

# points=np.array(gps)

# from scipy.spatial import Voronoi, voronoi_plot_2d
# vor = Voronoi(points)

# import matplotlib.pyplot as plt
# voronoi_plot_2d(vor)
# plt.show()

col_a = (0,0,255)
col_b = (255,255,0)
col_c = (255,0,0)

gmap = gmplot.GoogleMapPlotter(gps_centre[0], gps_centre[1], 16)

lons = []
lats = []
cols = []

for i,tt in enumerate(temp):
    t = tt[1]
    n = 750
    x, y = (0,0)
    gps_index = 100+i

    x, y = tt[0][1]
    scale = 200
    ##print tt[0][0]
    t-=min_temp
    t/=max_temp-min_temp

    if t>1: t=1
    if t<0: t=0

    col = heatmap_colour(t)
    col[0]*=255
    col[1]*=255
    col[2]*=255

    lons.append(y)
    lats.append(x)
    cols.append('#%02x%02x%02x'%(col[0],col[1],col[2]))
    #print x,y

    gmap.circle(x,y,4,c='#%02x%02x%02x'%(col[0],col[1],col[2]),face_alpha=0.1,edge_alpha=0.1)

    #plt.scatter(x, y, c='#%02x%02x%02x'%col, s=scale,
    #                alpha=0.3, edgecolors='none')
    

#gmap.heatmap(lats, lons)
#gmap.plot(lats, lons, cols, edge_width=10)

#plt.xlabel("latitude")
#plt.ylabel("longitude")
#plt.title("Sea temperature by GPS position")

#plt.grid(True)

#plt.show()

####################################################
# add in sonic map

# f = open("maprender/mapswansea.json","r")
# layers = json.loads(f.read())
# f.close()

# for layer in layers:
#     for zone in layer["zones"]:
#         print(zone["name"])
#         lats = []
#         lngs = []
#         centre = [0,0]
#         for latlng in zone["vertices"][0]:
#             centre[0]+=float(latlng["lat"])
#             centre[1]+=float(latlng["lng"])
#             lats.append(float(latlng["lat"]))
#             lngs.append(float(latlng["lng"]))

#         gmap.polygon(lats, lngs, zone["color"])

#######################################################


gmap.draw("mymap.html")
