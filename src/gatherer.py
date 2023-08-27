from arx.arx_collect import arxiv_gather
from model.oracle import Oracle


class gatherer:
    def __init__(self):
        pass

    def gather(self):
        arxs = arxiv_gather()
        collection,pth = arxs.main()
        
        if len(collection) > 0: 
            generate = Oracle(pth)
            generate.generator()
        elif len(collection) < 1:    
            print('No research on that topic, please try again...')
        #print(collection)
        #return collection
        pass

if __name__ == "__main__":
    gath = gatherer()
    gath.gather()
