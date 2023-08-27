import os

import pandas as pd
from dotenv import load_dotenv
from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from model.templates import business_template, research_template

load_dotenv()


class Oracle:

    post_doc_template = research_template

    business_analyst_template = business_template

    def __init__(self, path):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.df = pd.read_csv(path)
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key, model="gpt-4", temperature=0.6
        )
        self.categories = self.df.category.unique()
        pass

    def ctg_choose(self):

        print("for given query papers found it in the following categories:\n")
        for index, item in enumerate(self.categories, start=1):
            print(f"{index}. {item}")

        try:
            choice = int(
                input("\nPlease enter a number corresponding to your choice: ")
            )
            if 1 <= choice <= len(self.categories):
                return self.categories[choice - 1]
            else:
                print(
                    "Invalid choice. Please enter a number between 1 and {}.".format(
                        len(self.categories)
                    )
                )
        except ValueError:
            print("Please enter a valid number.")

        print(f"You have choosen: {choice}")

        return choice

    def pre_processor(self):

        df = self.df.drop(columns=["Unnamed: 0"])
        df["title_author_abstract"] = df.agg(
            "Title is: {0[title]}. Authors are: {0[authors]}. Summary is: {0[summary]}".format,
            axis=1,
        )
        df_grouped = (
            df.groupby("category")["title_author_abstract"]
            .agg("\n__Next Article__: ".join)
            .reset_index()
        )

        ctg = self.ctg_choose()

        articles = ""
        category = ""

        vals = df_grouped.to_dict("records")
        for i in vals:
            if i["category"] == ctg:  # change per user input
                category = i["category"]
                articles = i["title_author_abstract"]

        # return f'Research category is {category}. \n These are the titles, authors, and abstracts of these research articles {articles}:\n'
        return category, articles

    def generator(self):

        postdoc_prompt = ChatPromptTemplate.from_template(
            self.post_doc_template
        )

        chain_one = LLMChain(
            llm=self.llm, prompt=postdoc_prompt, output_key="postdoc_report"
        )

        bussines_analyst_prompt = ChatPromptTemplate.from_template(
            self.business_analyst_template
        )

        chain_two = LLMChain(
            llm=self.llm,
            prompt=bussines_analyst_prompt,
            output_key="business_brief",
        )

        overall_chain = SequentialChain(
            chains=[chain_one, chain_two],
            input_variables=["category", "articles"],
            output_variables=["postdoc_report", "business_brief"],
            verbose=True,
        )

        docs = self.pre_processor()
        gens = overall_chain({"category": docs[0], "articles": docs[1]})

        self.print_report(
            gens["category"], gens["postdoc_report"], gens["business_brief"]
        )

        return gens

    def print_report(self, category, academic, business):

        print("-" * 80)
        print(f'{" " * 35} REPORT')
        print("-" * 80)

        # Category title
        print(f'{"*" * 5} Category {"*" * 5}')
        print(f"For the chosen category: {category}")
        print()

        # Academic evaluation
        print(f'{"=" * 5} Academic Evaluation {"=" * 5}')
        print(
            f"This is the critical evaluation from an academic perspective:\n{academic}"
        )
        print()

        # Business evaluation
        print(f'{"+" * 5} Business Evaluation {"+" * 5}')
        print(
            f"This is the critical evaluation from a business perspective:\n{business}"
        )

        # Report ending
        print("-" * 80)
        print(f'{" " * 28} END OF REPORT')
        print("-" * 80)
