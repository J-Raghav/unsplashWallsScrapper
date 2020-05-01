import requests
from bs4 import BeautifulSoup
from os import mkdir,listdir,path

doc = '''
Features :-
	
	1. These script can download images from unsplash by inputing keyword
	2. It can keep track of how many images are downloaded and total images which can be downloaded
	3. It can save urls of particular tags so it dont need to request again

'''
print(doc)

def userInput():
	inpt = input('Search term followed by number of required images(<item> <num>) :- ').split()
	tag, n = '-'.join(inpt[:-1]), int(inpt[-1])
	return tag, n
	
	
def request(url):
	try:
		res = requests.get(url)
		return res
	except Exception as e:
		raise Exception('Something went wrong: '+ e.__doc__)


def writeFile(query,urls):
	try:
		with open(f'imgs/{query}/urls.txt','w') as f:
			f.write('\n'.join(urls))
			
			
	except Exception as e:
		raise Exception('Something went wrong: '+ e.__doc__)
		

def readFile(query):
	try:
		with open(f'imgs/{query}/urls.txt','r') as f:
			urls = [i.rstrip() for i in f.readlines()]
			return urls
	except FileNotFoundError:
		return []
	except Exception as e:
		raise Exception('Something went wrong: '+ e.__doc__)
		

def download(query,index,url):
	res = request(url)
	name = f'{query}{index+1}.jpeg'
	try:
		with open(f'imgs/{query}/{name}','wb') as f:
			f.write(res.content)
			print(f'{name} downloaded')
			return True
	except Exception as e:
		print(f"Can't download {name} : {e.__doc__}")
		return False


class ScrapUnsplash:
	
	def __init__(self,query): 
		self.query = query
		self.imgUrls = []
		try :
			mkdir('imgs/'+query)
		except:
			pass
		urls = readFile(query)
		if urls:
			self.imgUrls = urls
		else:
			self.scrapeUrls()
		
		self.setDownloaded()
		
		print(f'\nTotal {len(self.imgUrls)} found,\n{len(self.downloaded)} already downloaded!\n')
	

	def scrapeUrls(self):
		baseUrl = 'https://unsplash.com'
		q = self.query
		url =  baseUrl + '/search/photos/' + q
		res = request(url)
		if res:
			a_s = BeautifulSoup(res.text,'html.parser').find_all('a')
			self.imgUrls = [ baseUrl + a['href'] + '/download?force=true' for a in a_s if a['href'][0:7] == '/photos']
			writeFile(q,self.imgUrls)
			
		else:
			raise Exception('Something went wrong: '+ res.status_code)
	
	def getImgUrls(self,n=None):
		urls = [(self.imgUrls[i],i) for i in range(len(self.imgUrls)) if (i+1) not in self.downloaded]
		if n is None:
			return urls
		return urls[:n]

	
	def setDownloaded(self):	
		self.downloaded = { int(i.split('.')[0][-1]) for i in listdir(f'imgs/{self.query}') if path.isfile(f'imgs/{self.query}/{i}') and  i != 'urls.txt' }
		
		
	def download(self,n=1):
		urls = dict(self.getImgUrls(n))
		cnt = 0
		for i in urls:
			if download(self.query,urls[i],i):
				self.downloaded.add(urls[i])
			cnt+=1
		print(f'\nSummary {cnt}/{len(urls)} Downloaded Succesfully,\nYou can download {len(self.imgUrls)-len(self.downloaded)} more images for these tag.')

try:
	mkdir(imgs)
except:
	pass


inpt = input('Search term :- ').split()
tag = '-'.join(inpt)
obj = ScrapUnsplash(tag)
n = int(input('Number of images to download:- '))
print()
obj.download(n)

