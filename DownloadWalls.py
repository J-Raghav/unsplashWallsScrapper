import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from os import mkdir
path = 'https://unsplash.com/search/photos/'
try:
	tag,n = input('Search term followed by number of required images(item <num>)\n').split()
	n=int(n)
except:
	print('Invalid Input using default input "cool 3"')
	tag,n='cool',3
try:
	mkdir('./imgs')
except :
	pass
mkdir(f'./imgs/{tag}')
url = path + tag
html = requests.get(url)
soup = BeautifulSoup(html.text,'html.parser')	
a_s = soup.find_all('a')
urls = ['https://unsplash.com'+a['href']+'/download?force=true' for a in a_s if a['href'][0:7]=='/photos']
print(len(urls))

for url in urls[:n]:
	 
	try:
		res = requests.get(url)
		res.raise_for_status()
		
	except HTTPError as httpe:
		print(f'Err 0: {httpe}')
	except Exception as e:
		print(f'Err 1: {e}')
	else:
		print(res.status_code)
	
	try:
		with open(f'./imgs/{tag}/{tag}{urls.index(url)+1}.jpg','wb') as file:
			file.write(res.content)
		
	except Exception as e:
		print(f'Err 21: {e}')
	else:
		print('Done')
