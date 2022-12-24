from arx.arx_collect import arxiv_gather


class gatherer:
    def __init__(self):
        pass

    def gather(self):
        arxs = arxiv_gather()
        collection = arxs.main()

        print(collection)
        return collection


if __name__ == "__main__":
    gath = gatherer()
    gath.gather()
