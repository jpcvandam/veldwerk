#startdatum= meteo.index[0][0]
#begindag = str(startdatum)
#index = pd.date_range(begindag, periods=len(meteo), freq='H')
#druk = meteo['P'].values
#drukframe = pd.Series(druk, index=index)

#Neerslag = meteo['RH']/10.0

#t2897 = pd.read_csv(werkmap +'sws_t2897_150922194951_T2897.csv', skiprows=63, index_col=[0])
#print t2897
#waterdruk = t2897['Druk[cm]']
#waterdrukarray = t2897['Druk[cm]'].values/1000.0

#indexmeet=waterdruk.index.values
#for i in range(1, len(indexmeet)-1):
#    indexmeet[i]= pd.to_datetime(indexmeet[i])

#waterdrukframe = pd.Series(waterdrukarray, index=indexmeet)
#gecompenseerd = waterdrukframe - drukframe
