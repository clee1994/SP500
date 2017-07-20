#the yahoo_quote_download package comes from 
#https://github.com/c0redumb/yahoo_quote_download

from yahoo_quote_download import yqd
from stocks import stocks
import datetime 
import numpy as np
import pickle

start = '20070101'
end = str(datetime.date.today()).replace("-","")

tol_level = 0.1

dates = np.arange(datetime.datetime.strptime(start,"%Y%m%d"), datetime.date.today(), datetime.timedelta(days=1)).astype(datetime.datetime)
prices = np.empty((len(dates),len(stocks)))
prices[:] = np.NaN

for i in range(len(stocks)):
	print(stocks[i])
	raw_data = yqd.load_yahoo_quote(stocks[i], start, end)
	raw_data = [x.split(',') for x in raw_data]
	for cline in raw_data:
		try:
			ind = np.where(dates == datetime.datetime.strptime(cline[0],"%Y-%m-%d"))
			prices[ind[0][0],i] = float(cline[5])
		except:
			pass

#remove non trading days
indices = np.where(np.sum(np.isnan(prices),axis=1)!=505)
prices = prices[indices[0],:]
dates = dates[indices[0]]

#remove companies with insufficient info
indices = np.where(np.divide(np.sum(np.isnan(prices),axis=0),len(dates))<tol_level)
prices = prices[:, indices[0]]
names = np.array(stocks)[indices[0]]

lreturns = np.diff(np.log(prices),n=1, axis=0)
data = [prices, dates, names, lreturns]

pickle.dump((prices, dates, names, lreturns), open( "SP500.p", "wb" ) )



