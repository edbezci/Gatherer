import arxiv
import pandas as pd

from arx.arx_taxanomy import taxanomy


class arxiv_gather:
    def __init__(self):
        self.arx_storage: list[dict] = []

    def collect(self):

        query = input(
            "You are searching ArXiv!\nPlease enter a valid query for search\nFor instance:\n\tNatural Language Processing\n"
        )
        assert len(query) > 0, "please enter a query"

        max_results = int(
            input("Please enter the maximum amount of results to retrive...: ")
        )
        assert (
            0 < max_results <= 1500
        ), "please enter a number between 0 and 1500"

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        for res in search.results():
            self.arx_storage.append(
                {
                    "title": res.title,
                    "category": taxanomy.cats[res.primary_category],
                    "authors": res.authors,
                    "date": res.published,
                    "summary": res.summary,
                }
            )

    def clean_dataset(self) -> list:
        for d in self.arx_storage:
            d["authors"] = "; ".join([str(author) for author in d["authors"]])
        for d in self.arx_storage:
            d["date"] = d["date"].strftime("%d-%B-%Y")

        return self.arx_storage

    def main(self) -> pd.DataFrame:
        self.collect()
        if len(self.arx_storage) >= 1:
            print(
                f"There are {format(str(len(self.arx_storage)))} articles in the dataset."
            )
        else:
            print("There are not any articles in the dataset")
        cln_data = self.clean_dataset()

        return pd.DataFrame(cln_data)


if __name__ == "__main__":
    gth = arxiv_gather()
    gth.main()
