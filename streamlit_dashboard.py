import pandas as pd
import streamlit as st
import altair as alt


def main():

	page = st.sidebar.selectbox("Choose the Test Type", ["PCR","Rapid"])

	if page == 'PCR':
		df = load_data(type_='PCR')
	elif page == 'Rapid':
		df = load_data(type_='Rapid')

	st.title("{} Test Monitoring Dashboard".format(page))
	
	viz_type_filter = st.selectbox("Viz Type Filter", ['Daily','Cummulative'],0)

	if viz_type_filter == 'Daily':
		st.markdown("> Chart in this page shows the comparison of number of respondents who is tested and not tested")
		st.write("#Respondents: {}".format(len(df)))
		
		variable_filter = st.selectbox("Variable Filter", ['No Filter','Region',"Respondent's Age","Respondent's Gender","Respondent's Wage"],0)

		if variable_filter == 'No Filter':
			visualize_is_tested_comparison(df,None)
		elif variable_filter == 'Region':
			visualize_is_tested_comparison(df,'region')
		elif variable_filter == "Respondent's Age":
			visualize_is_tested_comparison(df,'age')
		elif variable_filter == "Respondent's Gender":
			visualize_is_tested_comparison(df,'gender')
		elif variable_filter == "Respondent's Wage":
			visualize_is_tested_comparison(df,'wage')
		else:
			st.write("Work in Progress..")


	elif viz_type_filter == 'Cummulative':
		st.markdown("> Charts in this page are generated based on accumulated data up to the desired date filter")

		date_filter = st.date_input('Date', max(df['date']))

		df_filter = df[df['date']<=date_filter]

		#Show Total Survey Data
		st.write("#Respondents: {}".format(len(df_filter)))

		#Show Cummulative Charts
		visualize_cummulative_charts(df_filter)

			
def load_data(type_):
	df = pd.read_csv('survey_data.csv')

	if type_=='PCR':
		df = df[df['type']=='pcr'].reset_index(drop=True)
	else:
		df = df[df['type']=='rapid'].reset_index(drop=True)

	df['date'] = pd.to_datetime(df['date']).dt.date

	return df


def visualize_is_tested_comparison(df,variable):
	
	if variable==None:
		df_grouped = df.groupby(['date','is_tested']).size().reset_index(name='count')

		bars = alt.Chart(df_grouped).mark_bar().encode(
			x = alt.X('date:N'),
			y = alt.Y('sum(count):Q', stack='zero',title='count')
			)

		group_bars = alt.Chart(df_grouped).mark_bar().encode(
			x = alt.X('date:N'),
			y = alt.Y('sum(count):Q', stack='zero',title='count'),
			tooltip = [alt.Tooltip('sum(count):Q',title='count')],
			color = alt.Color('is_tested')
			)

		text = bars.mark_text(dy=-10).encode(
			text = 'sum(count):Q'
			)

		group_text = alt.Chart(df_grouped).mark_text(dy=12,color='white').encode(
			x = alt.X('date:N'),
			y = alt.Y('sum(count):Q', stack='zero'),
			detail = 'is_tested:N',
			text = alt.Text('sum(count):Q')
			)

		st.altair_chart((group_bars + text + group_text).properties(height=800,width=800,title='Comparison Between Sales of Company X & Y Across Time'))

	else:

		for _type in df[variable].unique():
			df_temp = df[df[variable]==_type]
			df_grouped = df_temp.groupby(['date','is_tested']).size().reset_index(name='count')

			bars = alt.Chart(df_grouped).mark_bar().encode(
				x = alt.X('date:N'),
				y = alt.Y('sum(count):Q', stack='zero',title='count')
				)

			group_bars = alt.Chart(df_grouped).mark_bar().encode(
				x = alt.X('date:N'),
				y = alt.Y('sum(count):Q', stack='zero',title='count'),
				tooltip = [alt.Tooltip('sum(count):Q',title='count')],
				color = alt.Color('is_tested')
				)

			text = bars.mark_text(dy=-10).encode(
				text = 'sum(count):Q'
				)

			group_text = alt.Chart(df_grouped).mark_text(dy=12,color='white').encode(
				x = alt.X('date:N'),
				y = alt.Y('sum(count):Q', stack='zero'),
				detail = 'is_tested:N',
				text = alt.Text('sum(count):Q')
				)

			st.altair_chart((group_bars + text + group_text).properties(height=800,width=800,title='Comparison Between Sales of Company X & Y Across Time for value: {}'.format(_type)))


def visualize_cummulative_charts(df_filter):

	#Visualize Company is_tested
	is_tested_is_tested = df_filter['is_tested'].value_counts().reset_index()
	is_tested_chart = alt.Chart(is_tested_is_tested).mark_bar().encode(
		x = alt.X('index',title='is_tested',sort=['Influencer', 'Facebook']),
		y = alt.Y('is_tested',title='Count'),
		tooltip = [alt.Tooltip('is_tested',title='count')],
		color = alt.value('darkorange')
		).properties(
	    title='is_tested Distribution'
		)
	st.altair_chart(is_tested_chart.properties(height=400,width=600))


	#Visualize Item Price
	item_price_is_tested = df_filter['wage'].value_counts().reset_index()
	item_price_chart = alt.Chart(item_price_is_tested).mark_bar().encode(
		x = alt.X('index',title="Respondent's Wage",sort=['Less than 10 million','10 - 25 million','25 - 50 million','50 - 100 million','100 - 250 million','250 - 500 million','500+ million']),
		y = alt.Y('wage',title='Count'),
		tooltip = [alt.Tooltip('wage',title='count')],
		color = alt.value('darkorange')
		).properties(
	    title="Respondent's Wage Distribution"
		)
	st.altair_chart(item_price_chart.properties(height=400,width=600))


	#Visualize Age
	age_is_tested = df_filter['age'].value_counts().reset_index()
	age_chart = alt.Chart(age_is_tested).mark_bar().encode(
		x = alt.X('index',title="Respondent's Age",sort=['18-30', '30-50','50+']),
		y = alt.Y('age',title='Count'),
		tooltip = [alt.Tooltip('age',title='count')],
		color = alt.value('darkorange')
		).properties(
	    title="Respondent's Age Distribution"
		)
	st.altair_chart(age_chart.properties(height=400,width=600))


	#Visualize Gender
	gender_is_tested = df_filter['gender'].value_counts().reset_index()
	gender_chart = alt.Chart(gender_is_tested).mark_bar().encode(
		x = alt.X('index',title="Respondent's Gender",sort=['Female', 'Male']),
		y = alt.Y('gender',title='Count'),
		tooltip = [alt.Tooltip('gender',title='count')],
		color = alt.condition(
		alt.datum.index == 'Male',  
		alt.value('darkblue'),    
		alt.value('pink')   
		)
		).properties(
	    title="Respondent's Gender Distribution"
		)
	st.altair_chart(gender_chart.properties(height=400,width=600))


	#Visualize Ditribution of Region
	region_is_tested = df_filter['region'].value_counts().reset_index()
	region_chart = alt.Chart(region_is_tested).mark_bar().encode(
		x = alt.X('index',title='Region'),
		y = alt.Y('region',title='Count'),
		tooltip = [alt.Tooltip('region',title='count')],
		color = alt.value('darkorange')
		).properties(
	    title='Region Distribution'
		)
	st.altair_chart(region_chart.properties(height=400,width=600))


if __name__ == '__main__':
	main()
