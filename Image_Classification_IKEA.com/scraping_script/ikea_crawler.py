
# # Scraping images from www.ikea.com

import requests
import os

# image url dictionary for 4 objects, using set() to eliminate duplicate links
d = {
    'chair':set(),
    'bed':set(),
    'wardrobe':set(),
    'couch':set()
    }

'''
url = {
    
    'chair': 'https://sik.search.blue.cdtapps.com/in/en/search-result-page/more-products?sessionId=8a5f6982-3996-4065-bab7-6b1afc97e304&q=chair&start=0&end=2000&sort=RELEVANCE',
    'bed' : 'https://sik.search.blue.cdtapps.com/in/en/search-result-page/more-products?sessionId=8a5f6982-3996-4065-bab7-6b1afc97e304&q=bed&start=0&end=2000&sort=RELEVANCE'
    'table': 'https://sik.search.blue.cdtapps.com/in/en/search-result-page/more-products?sessionId=8a5f6982-3996-4065-bab7-6b1afc97e304&q=table&start=0&end=2000&sort=RELEVANCE'
    'couch' : 'https://sik.search.blue.cdtapps.com/in/en/search-result-page/more-products?sessionId=8a5f6982-3996-4065-bab7-6b1afc97e304&q=couch&start=0&end=2000&sort=RELEVANCE'
}
'''

# for each object
for o in list(d.keys()):
    

    # ikea.com link to objects from where images are fetched
    URL = 'https://sik.search.blue.cdtapps.com/in/en/search-result-page/more-products?sessionId=8a5f6982-3996-4065-bab7-6b1afc97e304&q='+o+'&start=0&end=2000&sort=RELEVANCE'
    
    # request image urls
    r = requests.get(url = URL) 

    # receive respose
    data = r.json() 
    
    # maximum number of images per object = 2000
    for j in range(2000):
            
        try:
            image_url = data['moreProducts']['productWindow'][j]['main_image_url']
            d[o].add(image_url)
            print('Scraping:',o,'_',j)
        
        except:
            print('No more images')
            break
        


# number of distinct images for every class
print(len(d['chair']))
print(len(d['wardrobe']))
print(len(d['couch']))
print(len(d['bed']))


# create directories
os.system('mkdir -p chair wardrobe couch bed')


# ## Write images in respective directories
c = 0
# iterating over objects
for o in list(d.keys()):
    # iterating over urls
    for i in d[o]:
        with open(o+'/'+o+'_'+str(c)+'.jpg', 'wb') as handle:
                response = requests.get(str(i), stream=True)

                if not response.ok:
                    print(response)

                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
                c += 1
    c=0


# ### Note: Bed is replaced by Table. Images for 'bed' contains a lot of irrelevant images and also images of couch.  Objects with maximum available images were selected.