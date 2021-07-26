import pandas as pd 
import time
import arxiv
import json
import os.path

import urllib.request
import urllib.parse


from itertools import chain, count
from pymed import PubMed



from dateutil.parser import parse
from datetime import datetime

class Gatherer:

    def __init__(self):
        self.__storage = []
        self.__corpus =[]
        pass

    def Gather(self):
        while True:
            try:
                response = int(input('Do you want to use:\nPubMed(1)\nArXiv(2)\nCORE(3)\nType 1 for Pubmed\nType 2 for ArXiv\nType 3 for CORE'))
            except:
                print('\033[1m'+'Please enter either 1,2 or 3...\nPlease start over and try again...'+'\033[1m')
                break
            if response == 1:
                self.__pubmedGather()
                break

            elif response == 2:
                self.__arxivGather()
                break
            elif response == 3:
                self.__COREGather()
                break

            else:
                print('\033[1m'+'Please enter either 1,2 or 3...\nPlease start over and try again...'+'\033[1m')
                break

    def __pubmedGather(self):
        start = time.time()
        while True:
            try:
                query = input("You are in PubMed\nPlease enter a valid query.\nFor instance:\n\tchildren[Title] AND (hasabstract[text] AND \"2019/09/07\"[PDAT] : \"2020/09/04\"[PDAT])\n")
                break
            except:
                print('Please enter a valid query.')        
        while True:
            try:
                max_results = int(input('Please enter the maximum amount of results to retrive...: '))
                break
            except:
                print('Please enter an integer...')
        pubmed = PubMed(tool="XXXXXX", email="XXXX@XXX.XXX") # customize your email/project name
        results = pubmed.query(query, max_results=max_results)
        pubmed_store = [article.toDict() for article in results] #if len(article.abstract) > 12
        pubmed_store = self.__prunePubmed(pubmed_store)
        end = time.time()
        if len(pubmed_store) > 1:
            print ('\033[1m'+ '{} articles are added to the dataset in {} seconds.'.format(str(len(pubmed_store)),round(end-start,2))+'\033[1m')
        else:
            print ('\033[1m'+ '{} article is added to the dataset in {} seconds.'.format(str(len(pubmed_store)),round(end-start,2))+'\033[1m')
        return self.__storage.extend(pubmed_store)

    def __arxivGather(self):
        start = time.time()
        arXivStore = []
        while True:
            try:
                query = input("You are in ArXiv!\nPlease enter a valid query for search\nFor instance:\n\tNatural Language Processing\n")
                break
            except:
                print('Please enter a valid query.') 
        while True:
            try:
                max_results = int(input('Please enter the maximum amount of results to retrive...: '))
                break
            except:
                print('Please enter an integer...')
        arXivStore.extend(arxiv.query(query=query, max_results=max_results, max_chunk_results=100000))
        # arXivStore = self.__pruneArXive(arXivStore)
        end = time.time()
        if len(arXivStore) > 1:
           print ('\033[1m'+ '{} articles are added to the dataset in {} seconds.'.format(str(len(arXivStore)),round(end-start,2))+'\033[1m')
        else:
            print ('\033[1m'+ '{} article is added to the dataset in {} seconds.'.format(str(len(arXivStore)),round(end-start,2))+'\033[1m')
        return self.__storage.extend(arXivStore)

    def __COREGather(self):
        start = time.time()
        coreStore = []
        while True:
            try:
                query = input("You are in CORE\nPlease enter a Query.\n")
                query = '(title:('+query+') OR description:('+query+'))'
                break
            except:
                print('Please enter a valid query.')        
        while True:
            try:
                max_results = int(input('Please enter the maximum amount of results to retrive...: '))
                break
            except:
                print('Please enter an integer...')

        endpoint = 'https://core.ac.uk/api-v2'
        api_key = 'XXXXXXXXXX'  #API KEY
        #defaults
        pagesize = 30
        page = 1
        method = '/articles/search'
        params = {
            'apiKey':api_key,
            'page':page,
            'pageSize':pagesize,
            'fulltext': 'false'
        }
        url = endpoint + method + '/' + urllib.parse.quote(query) + '?' + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url) as response:
            html = response.read()
        result = json.loads(html.decode('utf-8'))
        no_res = min(max_results,result['totalHits'])
        temp_store = []
        for res in range(1,int(no_res/pagesize)+1):
            params = {'apiKey':api_key,'page':res,'pageSize':pagesize,'fulltext': 'false'}
            url1 = endpoint + method + '/' + urllib.parse.quote(query) + '?' + urllib.parse.urlencode(params)
            with urllib.request.urlopen(url1) as response:
                html = response.read()
            temp_store.append(json.loads(html.decode('utf-8')))
        for i in temp_store:
            coreStore.extend(i['data'])
        end = time.time()
        if len(coreStore) > 1:
            print ('\033[1m'+ '{} articles are added to the dataset in {} seconds.'.format(str(len(coreStore)),round(end-start,2))+'\033[1m')
        else:
            print ('\033[1m'+ '{} article is added to the dataset in {} seconds.'.format(str(len(coreStore)),round(end-start,2))+'\033[1m')
        return self.__storage.extend(coreStore)
    
    
    def toDataFrame(self):
        frame = pd.DataFrame(self.__storage)
        try:
            return frame
        except:
            print('The object can\'t be converted into a DataFrame')

    def toCSV(self):
        name = input('What is the file name to save?\n(please exlude .csv)\nWhite spaces will be filled with \'_\' \n')
        name = name.replace(' ', '_')
        name = name + '.csv'
        frame = pd.DataFrame(self.__storage)
        try:
            return frame.to_csv(name)
        except Exception as e:
            print('The object can\'t be converted into a csv file.\n'+e)
        finally:
            if os.path.exists(name):
                print('\033[1m'+ '{}  is succesfully created.'.format(name)+'\033[1m' )
    
    def toJSON(self):
        name = input('What is the file name to save?\n(please exlude .json)\nWhite spaces will be filled with \'_\' \n')
        name = name.replace(' ', '_')
        name += '.json'
        try: 
            with open(name, 'w') as file:
                json.dump(self.__storage , file, indent=4, sort_keys=True, default=str)
        except Exception as e:
            print('The object can\'t be converted into a json file.\n'+e)

        finally:
            if os.path.exists(name):
                print('\033[1m'+ '{}  is succesfully created.'.format(name)+'\033[1m' )

    def toCorpus(self):
        columns = ['abstract','description','title','Abstract','Title','Description']
        store =[]
        for i in self.__storage:
            try:
                store.append({k: i[k] for k in columns if i.get(k) is not None})
            #try:
            #    store.extend([i[k] for k in columns])
            except:
               print('looking for the keys')
        return self.__corpus.extend(store)
    
    def CorpustoDataFrame(self):
        frame = pd.DataFrame(self.__corpus)
        try:
            return frame
        except:
            print('The object can\'t be converted into a DataFrame')

    @property
    def store(self):
        return self.__storage

    @store.setter
    def store(self,value):
        self.__storage += value
    
    @store.deleter
    def store(self):
        del self.__storage

    @staticmethod
    def __prunePubmed(store):
        for d in store:
            for t in d['authors']:
                del t['initials']
                try:
                    d['authors'] = str.join(',', t.values())
                except:
                    d['authors'] = "NoAuthor"
        return store

    @staticmethod
    def __pruneArXive(store):
        for d in store:
            if d['journal_reference'] == None:
                d['journal_reference'] = 'preprint'
        for d in store:
            d['authors'] = ' '.join([str(author) for author in d['authors']]) 
        for d in store:
            newentry = parse(d['publication_date'])
            d['publication_date'] = newentry.strftime("%d-%B-%Y")
        return store

    def __repr__(self):
        return '\n'.join(str(i) for i in self.__storage)
    
    def __str__(self):
        if len(self.__storage) == 0:
            return 'There are no articles in the dataset to print!'  
        elif  len(self.__storage) >= 5:
                items = [i['title'] for i in self.__storage[0:5]]
        else:
            items = [i['title'] for i in self.__storage]
        print('There are {} articles stored in this dataset.'.format(len(self.__storage)), end='\n\tTitles of the first 5 articles are:\n')
        return '\n'.join(items)

    def __add__(self,other):
        assert isinstance(other, type(self))
        NewDataset = self.__class__()
        NewDataset.store = self.store
        NewDataset.store = other.store
        return NewDataset








    
    











