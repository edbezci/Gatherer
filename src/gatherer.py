from arx.arx_collect import arxivGather


class Gatherer:
    def __init__(self):
        pass

    def gather(self):
        arxs = arxivGather()
        collection = arxs.main()

        print(collection)


if __name__ == "__main__":
    gath = Gatherer()
    gath.gather()
