import math

def dystans(lat1, lon1, lat2,lon2): #funkcja liczy dystans miedzy dwoma koordynatami

    lat1= math.radians(lat1)
    lon1 =math.radians(lon1)
    lat2= math.radians(lat2)
    lon2= math.radians(lon2)#zmiana stopni na promien

    dlon= lon2-lon1
    dlat=lat2-lat1
    a= math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c= 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    dystans=6371*c # srednica ziemi 
    return dystans

def NN(lat, lon, punkty): #funkcja nearest neighbor dla danego punktu
    min_dystans = float('inf')
    NN= None
    for punkt in punkty:
        d= dystans(lat, lon,punkt[0], punkt[1])
        if d<min_dystans: #zmien sasiada na nowego jezeli dystans jest mniejszy od obecnego
            min_dystans=d
            NN=punkt
    return NN

    #Punkty
punkty =[
    (26.0347, 50.5089, "Bahrain"),
    (21.6334, 39.1035, "Saudi Arabia"),
    (-37.8409, 144.9680, "Australia"),
    (40.4083, 49.8622, "Azerbaijan"),
    (25.9566, -80.2310, "Miami"),
    (44.3447, 11.7155, "Imola"),
    (43.7347, 7.4197, "Monaco"),
    (41.5728, 2.2610, "Spain"),
    (45.5079, -73.5290, "Canada"),
    (47.2183, 14.7060, "Austria"),
    (52.0786, -1.0169, "Great Britain"),
    (47.5106, 19.2556, "Hungary"),
    (50.4373, 5.9750, "Belgium"),
    (52.2544, 4.5397, "Netherlands"),
    (45.6237, 9.2844, "Monza"),
    (1.2931, 103.8550, "Singapore"),
    (34.8414, 136.5460, "Japan"),
    (25.4861, 51.4523, "Qatar"),
    (30.1375, -97.6400, "Cota"),
    (19.4052, -99.0930, "Mexico"),
    (-23.7010, -46.6980, "Brazil"),
    (36.1068, -115.1680, "Las Vegas"),
    (24.4749, 54.6038, "Abu Dhabi")
]


dystans_calkowity =0
obecny_punkt=punkty[0]
sciezka=[obecny_punkt]
punkty.remove(obecny_punkt)
while len(punkty)>0:   #powtarzaj az odwiedzisz wszytskie punkty
    nastepny_punkt= NN(obecny_punkt[0],obecny_punkt[1],punkty)
    sciezka.append(nastepny_punkt)
    punkty.remove(nastepny_punkt)
    dystans_calkowity+=dystans(obecny_punkt[0], obecny_punkt[1],nastepny_punkt[0], nastepny_punkt[0])
    obecny_punkt=nastepny_punkt

print('kolejnosc punktow')
for punkt in sciezka:
    print(punkt)

print('dystans calkowity: %.2f kilometra'% dystans_calkowity)