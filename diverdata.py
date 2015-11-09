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
from pandas.io.date_converters import parse_date_time

werkmap = '/home/john/Documenten/Afstuderen_Acacia_water/Data/Veldwerk/den_helder/Excel/'
pad_meteo = '/home/john/Documenten/Afstuderen_Acacia_water/Data/Veldwerk/den_helder/Meteo_De_Kooy/'
pad_plots = '/home/john/Documenten/Afstuderen_Acacia_water/Data/Veldwerk/den_helder/plots/'

meteobestand = 'KNMI_20151108_hourly.txt'
diverbestand = 'sws_t2897_151030_T2897.csv'
divernummer = 'T2897'

def datehour_parser(ymd,hours):
    try:
        return np.array([datetime.datetime.strptime(d,'%Y%m%d') + datetime.timedelta(hours=int(h)) for d,h in zip(ymd,hours)])
    except Exception as e:
        print e   


def dateparser(dates):
  return [datetime.datetime.strptime(d,'%Y/%m/%d %H:%M:%S') for d in dates]
 
#url = 'http://www.knmi.nl/klimatologie/uurgegevens/getdata_uur.cgi'
 
# Bij uurgegevens kan er een carriage return (\r) tussen de kolommen zitten
with open(pad_meteo+meteobestand,'rb') as f:
    text = f.read().translate(None,'\r')
    io = StringIO.StringIO(text)
    data = pd.read_csv(io,
                         header=None,
                         skiprows=34,
                         skipinitialspace=True,
                         comment = '#',
                         index_col = 'Datum',
                         parse_dates={'Datum': [1,2]}, #kolommen in het meteobestand
                         date_parser = datehour_parser)
    print data
    meteo = data.resample('15T', fill_method='pad')

print meteo

#sws_t2904_150922194909_T2904.csv
#sws_t2905_150922194831_T2905.csv
diverdata = pd.read_csv(werkmap + diverbestand, skiprows=63, decimal=',', index_col=[0], parse_dates = [0], date_parser = dateparser)#, dtype={'Specifieke geleidbaarheid':np.float64}, engine= 'c', encoding='utf-8')
print diverdata

#tijdzones compenseren
meteo=meteo.tz_localize('UTC')
meteo=meteo.tz_convert('Europe/Amsterdam')
diverdata=diverdata.tz_localize('CET', ambiguous='NaT')
diverdata=diverdata.tz_convert('Europe/Amsterdam')
#print meteo.index, 'meteo goede tijdzone'
#print diverdata.index, 'diver goede tijdzone'
print diverdata
luchtdruk = meteo[14] / 9.80638
print 'luchtdruk', luchtdruk
waterdruk = diverdata['Druk[cm]']#/1000.0
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
gecompenseerd.to_csv(divernummer + '_gecompenseerd.csv', index=True, sep=',')

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
plt.title('Gemeten waterstand ' + divernummer)
pylab.savefig(pad_plots + 'waterstandsplot_'+ divernummer + '.png')
pylab.close()


#print diverdata['Specifieke geleidbaarheid']

#geleidbaarheid
plt.figure(); diverdata['Specifieke geleidbaarheid'].plot(label='Specifieke geleidbaarheid'); 
plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$microS/cm$')
plt.xlabel('Tijd')
plt.title('Geleidbaarheid')
pylab.savefig(pad_plots + 'EC_spec_plot_' + divernummer + '.png')
pylab.close()

#neerslag
plt.figure(); neerslag.plot(kind='bar', label='neerslag');
plt.legend(loc='upper center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$mm$')
plt.xlabel('Tijd')
plt.title('Neerslag' + divernummer)
pylab.savefig(pad_plots + 'neerslag_' + divernummer + '.png')
pylab.close()

#handmetingen
print diverdata['EC ondiep (microS/cm)'].dropna()
print diverdata['EC diep  (microS/cm)'].dropna()

plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$mS/cm$')
plt.xlabel('Tijd')
plt.title('Handmetingen geleidbaarheid ' + divernummer)
pylab.savefig(pad_plots + 'EChandmetingen_'+ divernummer + '.png')
pylab.close()


#plot geleidbaarheid
plt.figure(); diverdata['1:Geleidbaarheid[mS/cm]'].plot(label='Geleidbaarheid'); diverdata['Specifieke geleidbaarheid'].plot(label='Specifieke geleidbaarheid'); neerslag.plot(secondary_y=True, label='Neerslag'); #2897['EC ondiep (microS/cm)'].plot(kind='scatter');
#plt.figure(); diverdata['Specifieke geleidbaarheid'].plot(); 
#plt.figure(); diverdata['EC ondiep (microS/cm)'].plot(); 
#plt.figure(); diverdata['EC diep (microS/cm)'].plot();
plt.legend(loc='lower center', shadow=True, fontsize='x-large')
ax = pylab.gca()
ax.set_ylabel('$microS/cm$')
ax.right = neerslag.plot(secondary_y=True)
ax.right.set_ylabel('$mm$') 
plt.xlabel('Tijd')
plt.title('Geleidbaarheid ' + divernummer)
pylab.savefig(pad_plots + 'ECplot_'+ divernummer + '.png')
pylab.close()