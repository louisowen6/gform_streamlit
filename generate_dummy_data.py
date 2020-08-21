import pandas as pd
import random

if __name__ == "__main__":

	date_list = ['01-05-2020','02-05-2020','03-05-2020','04-05-2020','05-05-2020','05-05-2020','07-05-2020','08-05-2020','09-05-2020','10-05-2020'
	,'11-05-2020','12-05-2020','13-05-2020','14-05-2020','15-05-2020','16-05-2020','17-05-2020','18-05-2020','19-05-2020','20-05-2020','21-05-2020'
	,'22-05-2020','23-05-2020','24-05-2020','25-05-2020','26-05-2020','27-05-2020','28-05-2020','29-05-2020','30-05-2020','31-05-2020'
	,'01-06-2020','02-06-2020','03-06-2020','04-06-2020','05-06-2020','06-06-2020','07-06-2020','08-06-2020','09-06-2020','10-06-2020','11-06-2020'
	,'12-06-2020','13-06-2020','14-06-2020','15-06-2020','16-06-2020','17-06-2020','18-06-2020','19-06-2020','20-06-2020','21-06-2020','22-06-2020'
	,'23-06-2020','24-06-2020','25-06-2020']

	region_list = ['Jakarta Pusat','Jakarta Barat','Jakarta Timur','Jakarta Selatan','Jakarta Utara']

	is_test_list = ['Ya','Tidak']

	age_list = ['18 - 30 tahun','31 - 50 tahun','Di atas 50 tahun']

	gender_list = ['Laki-laki','Perempuan']

	wage_list = ['Lebih kecil dari Rp 3.000.000','Rp 3.000.000 - Rp 5.000.000','Rp 5.000.001 - Rp 10.000.000','Rp 10.000.001-Rp 25.000.000','Lebih besar dari Rp 25.000.000']

	df = pd.DataFrame()
	for i in range(1000):
		df = df.append({
			'date':random.choice(date_list),
			'Dimanakah Letak Daerah Tempat Tinggal Anda?':random.choice(region_list),
			'Berapa Umur Anda?':random.choice(age_list),
			'Apakah Jenis Kelamin Anda?':random.choice(gender_list),
			'Berapakah Pendapatan Anda?':random.choice(wage_list),
			'Apakah Anda Pernah Melakukan PCR Test?':random.choice(is_test_list),
			},ignore_index=True)

	df['date'] = pd.to_datetime(df['date']).dt.date
	df = df.sort_values(by='date')

	df.to_csv('dummy_data_pcr_test.csv',index=False)


