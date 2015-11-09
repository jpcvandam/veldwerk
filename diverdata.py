#diverdata inlezen en compenseren voor druk, vervolgens plotten
#auteur: John van Dam
#datum: 19 oktober 2015
#cd ~/Documenten/Afstuderen_Acacia_water/Data/Veldwerk/den_helder

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil import tz
import numpy as np
import pylab
import pytz
import StringIO

werkmap = '/home/john/Documenten/Afstuderen_Acacia_water/Data/Veldwerk/den_helder/Excel/'
pad_meteo = '/home/john/Documenten/Afstuderen_Acacia_water/Data/Veldwerk/den_helder/Meteo_De_Kooy/'

def datehour_parser(ymd,hours):
    try:
        return np.array([datetime.datetime.strptime(d,'%Y%m%d') + datetime.timedelta(hours=int(h)) for d,h in zip(ymd,hours)])
    except Exception as e:
        print e   


def dateparser(dates):
  return [datetime.datetime.strptime(d,'%Y/%m/%d %H:%M:%S') for d in dates]
 
url = 'http://www.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi'
 
# Bij uurgegevens kan er een carriage return (\r) tussen de kolommen zitten
with open(pad_meteo+'KNMI_20151108_hourly.txt','rb') as f:
    text = f.read().translate(None,'\r')
    io = StringIO.StringIO(text)
    data = pd.read_csv(io,
                         header=None,
                         skipinitialspace=True,
                         comment = '#',
                         index_col = 'Datum',
                         parse_dates={'Datum': [1,2]},
                         date_parser = datehour_parser)
    #print data
    meteo = data.resample('15T', fill_method='pad')
meteo = pd.read_csv(pad_meteo+'KNMI_20151108_hourly.txt', parse_dates={'dates' : [1,2]},  skipinitialspace=True, index_col=[1,2])
print meteo

#sws_t2904_150922194909_T2904.csv
#sws_t2905_150922194831_T2905.csv
t2897 = pd.read_csv(werkmap +'sws_t2897_151030_T2897.csv', skiprows=63, index_col=[0], decimal=',', parse_dates = [0], date_parser = dateparser)#, dtype={'Specifieke geleidbaarheid':np.float64}, engine= 'c', encoding='utf-8')
print t2897

#tijdzones compenseren
meteo=meteo.tz_localize('UTC')
t2897=t2897.tz_localize('CET')
meteo=meteo.tz_convert('Europe/Amsterdam')
t2897=t2897.tz_convert('Europe/Amsterdam')
#print meteo.index, 'meteo goede tijdzone'
#print t2897.index, 'diver goede tijdzone'
print t2897
luchtdruk = meteo[14] / 9.80638
#print 'luchtdruk', luchtdruk
waterdruk = t2897['Druk[cm]']/1000.0
#print 'waterdruk', waterdruk
#print luchtdruk.index
#print waterdruk.index

neerslag = meteo[13]/10.0
#print 'neerslag', neerslag
#tijdzones compenseren
luchtdruk=luchtdruk.tz_convert('Europe/Amsterdam')
waterdruk=waterdruk.tz_convert('Europe/Amsterdam')
#print luchtdruk.index
#print waterdruk.index

#compensatie van waterdruk voor luchtdruk uitvoeren
gecompenseerd = waterdruk - luchtdruk #+ 43.733382 #translatie om te ijken op de plop -115
gecompenseerd.dropna(inplace=True)
#print gecompenseerd, 'gecompenseerd'
gecompenseerd.to_csv('t2897_gecompenseerd.csv', index=True, sep=',')

####################################################################################################
#plotten en plot opslaan

#waterstanden
plt.figure(); gecompenseerd.plot(label='Waterstanden'); neerslag.plot(secondary_y=True, label='Neerslag'); #secondary_y=True, 
plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$cm-mv$')
ax.right = neerslag.plot(secondary_y=True)
ax.right.set_ylabel('$mm$') 
plt.xlabel('Tijd')
plt.title('Gemeten waterstand T2897')
pylab.savefig('waterstandsplot_T2897.png')
pylab.close()

#plot geleidbaarheid
plt.figure(); t2897['1:Geleidbaarheid[mS/cm]'].plot(label='Geleidbaarheid'); t2897['Specifieke geleidbaarheid'].plot(label='Specifieke geleidbaarheid'); neerslag.plot(secondary_y=True, label='Neerslag'); #2897['EC ondiep (microS/cm)'].plot(kind='scatter');
#plt.figure(); t2897['Specifieke geleidbaarheid'].plot(); 
#plt.figure(); t2897['EC ondiep (microS/cm)'].plot(); 
#plt.figure(); t2897['EC diep (microS/cm)'].plot();
plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$microS/cm$')
ax.right = neerslag.plot(secondary_y=True)
ax.right.set_ylabel('$mm$') 
plt.xlabel('Tijd')
plt.title('Geleidbaarheid T2897')
pylab.savefig('ECplot_T2897.png')
pylab.close()
#print t2897['Specifieke geleidbaarheid']

#geleidbaarheid
plt.figure(); t2897['Specifieke geleidbaarheid'].plot(label='Specifieke geleidbaarheid'); 
plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$microS/cm$')
plt.xlabel('Tijd')
plt.title('Geleidbaarheid')
pylab.savefig('EC_spec_plot_T2897.png')
pylab.close()

#neerslag
plt.figure(); neerslag.plot(kind='bar', label='neerslag');
plt.legend(loc='upper center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$mm$')
plt.xlabel('Tijd')
plt.title('NeerslagT2897')
pylab.savefig('neerslag_T2897.png')
pylab.close()

#handmetingen
print t2897['EC ondiep (microS/cm)'].dropna()
print t2897['EC diep  (microS/cm)'].dropna()

plt.figure(); t2897['EC ondiep (microS/cm)'].plot(style='k--'); t2897['EC diep  (microS/cm)'].plot(style='k--');
plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$mS/cm$')
plt.xlabel('Tijd')
plt.title('Handmetingen geleidbaarheid T2897')
pylab.savefig('EChandmetingen_T2897.png')
pylab.close()

