from django.shortcuts import render
from django.http import HttpResponse
from geopy.geocoders import ArcGIS
nom=ArcGIS()
import folium
import pandas as pd
import math
def hom(request):
    return render(request,'hello.html',{'name':'Map'})
def location(request):
     src=request.POST['loc1']
     dst=request.POST['loc2']
     data=pd.read_csv("templates/out.csv",index_col=0)
     i=1
     while i:
          try:
               n=nom.geocode(src)
               m=nom.geocode(dst)
               map=folium.Map(location=[n.latitude,n.longitude],zoom_start=10,tiles="openstreetmap")
               fg=folium.FeatureGroup(name="my map")
               def weathers(we):
                    if we=="high":
                         return "red"
                    else:
                         return "green"
               points=[]
               for point in range(1,len(data["coordinates"])+1):
                    if data['weather'][point]=='low':
                         points.append(tuple([data["latitude"][point],data["longitude"][point]]))
               points.insert(0,(n.latitude,n.longitude))


               app=[]
               wo=[]
               ww=[]
               lis=points
               while len(lis)>1:
                    length=len(lis)
                    wo.append(lis[0])
                    for i in range(1,length):
                         dist=math.sqrt((lis[i][0]-lis[0][0])**2+(lis[i][1]-lis[0][1])**2)
                         app.append(dist)
                    mi=app.index(min(app))
                    wo.append(lis[mi+1])
                    lll=lis.copy()
                    for i in wo:
                         lll.remove(i)
                    lll.insert(0,wo.pop())
                    ww.append(wo)
                    app=[]
                    wo=[]
                    lis=lll.copy()
    
    
               e=[]
               for i in ww:
                    e.append(i[0])
               e.append(lis[0])
               e.append((m.latitude,m.longitude))
               for i in range(1,len(data["latitude"])+1):
                    ht="""<html>
                    <div>TIME:%s STATUS:%s</div>
                    </html>
                    """ % (data["time"][i],data['status'][i])
                    fg.add_child(folium.Marker(location=[data["latitude"][i],data["longitude"][i]],popup=folium.Popup(ht),icon=folium.Icon(color=weathers(data["weather"][i]))))
                    fg.add_child(folium.Marker(location=[n.latitude,n.longitude],popup="CURRENT LOCATION",icon=folium.Icon(color='black')))
                    fg.add_child(folium.Marker(location=[m.latitude,m.longitude],popup="DESTINATION LOCATION",icon=folium.Icon(color='black')))
                    map.add_child(fg)
                    folium.PolyLine(e,color='red',width=2.5,opacity=1).add_to(map)
               map.save("templates/result.html")
               i=0
               return render(request,'result.html')
          except:
               i=1
          

     
