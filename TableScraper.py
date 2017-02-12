'''
Scraping functions to fill an excel file with html tables content
Author : Alexandre Thissen
Date : 2017 February 11th
'''
# Imports 
import requests, xlwt
from bs4 import BeautifulSoup

# Function definition
def get_data_table(url, page): 
	url = url + str(page)
	response = requests.get(url)
	if response.status_code == 200: 
		soup = BeautifulSoup(response.content, 'lxml')
		table = soup.find('table')
		return table

def get_headings(table):
	headings = [th.get_text().strip(' \t\n\r') for th in table.find("tr").find_all("th")]
	return headings

def sort_html_table(table): 
	content = []
	for row in table.find_all('tr')[1:]: 
		new_row = [td.get_text().strip(' \t\n\r') for td in row.find_all('td')]
		content.append(new_row)
	return content

def export_excel(headings, content, name, path):
	book = xlwt.Workbook()
	sheet1 = book.add_sheet(name)

	row_title = sheet1.row(0)
	for i, el in enumerate(headings): 
		row_title.write(i,el)

	for n in xrange(len(content)): 
		row = sheet1.row(n+2)
		for i, el in enumerate(content[n]):
			row.write(i,el)

	book.save(path + name + '.xls')

# Main function
def main(): 
	# Parameters
	url = 'https://pharmacists.ab.ca/pharmacists-0?page='
	path = '/Users/athissen/Desktop/'
	name = 'AlbertaPharmacists'

	# Output
	content = []

	# Headers
	table = get_data_table(url,0)
	headings = get_headings(table)

	# Content
	for i in xrange(172):
		print 'page %s is being processed' % str(i)
		table = get_data_table(url,i)
		content += sort_html_table(table)

	# Export
	export_excel(headings, content, name, path)


if __name__ == '__main__': 
	main()

