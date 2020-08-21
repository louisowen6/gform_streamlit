import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Tutorial Louis-985b5d882f76.json', scope) #Change to your downloaded JSON file name 
client = gspread.authorize(creds)

#Change to your Google Sheets Name
spreadsheets = ['dummy_data_rapid_test','dummy_data_pcr_test']


def main(spreadsheets):

	df = pd.DataFrame()

	for spreadsheet in spreadsheets:
		#Open the Spreadsheet
		sh = client.open(spreadsheet)

		#Get all values in the first worksheet
		worksheet = sh.get_worksheet(0)
		data = worksheet.get_all_values()

		#Save the data inside the temporary pandas dataframe
		df_temp = pd.DataFrame(columns = [i for i in range(len(data[0]))])
		for i in range(1,len(data)):
			df_temp.loc[len(df_temp)] = data[i]
		
		#Convert column names
		column_names = data[0]
		df_temp.columns = [convert_column_names(x) for x in column_names]

		#Data Cleaning
		df_temp = df_temp.drop_duplicates().reset_index(drop=True)
		df_temp['is_tested'] = df_temp['is_tested'].replace({'Ya':'Yes','Tidak':'No'})
		df_temp['region'] = df_temp['region'].replace({'Jakarta Pusat':'Central Jakarta','Jakarta Barat':'West Jakarta','Jakarta Timur':'East Jakarta','Jakarta Utara':'North Jakarta','Jakarta Selatan':'South Jakarta'})
		df_temp['gender'] = df_temp['gender'].replace({'Laki-laki':'Male','Perempuan':'Female'})
		df_temp['age'] = df_temp['age'].replace({'18 - 30 tahun':'18-34','31 - 50 tahun':'31-50','Di atas 50 tahun':'50+'})
		df_temp['wage'] = df_temp['wage'].replace({'Lebih kecil dari Rp 3.000.000':'less than IDR 3 million',
		'Rp 3.000.000 - Rp 5.000.000':'IDR 3-5 million',
		'Rp 5.000.001 - Rp 10.000.000':'IDR 5-10 million',
		'Rp 10.000.001-Rp 25.000.000':'IDR 10-25 million',
		'Lebih besar dari Rp 25.000.000':'more than IDR 25 million'})

		#Feature Engineering
		if 'pcr' in spreadsheet:
			_type = 'pcr'
		else:
			_type = 'rapid'

		df_temp['type'] = _type
		
		#Convert to timestamp
		df_temp['date'] = pd.to_datetime(df_temp['date'])

		#Concat Dataframe
		df = pd.concat([df,df_temp])	

		#API Limit Handling
		time.sleep(5)


	df = df.sort_values(by=['date']).reset_index(drop=True)

	df.to_csv('survey_data.csv',index=False)


def convert_column_names(x):
	if x == 'Berapakah Pendapatan Anda?':
		return 'wage'
	elif x == 'Dimanakah Letak Daerah Tempat Tinggal Anda?':
		return 'region'
	elif x == 'Apakah Jenis Kelamin Anda?':
		return 'gender'
	elif x == 'Berapa Umur Anda?':
		return 'age'
	elif (x == 'Apakah Anda Pernah Melakukan PCR Test?') or (x == 'Apakah Anda Pernah Melakukan Rapid Test?'):
		return 'is_tested'
	else:
		return x


if __name__ == '__main__':
	print('Scraping Form Data')
	main(spreadsheets)	