import pandas as pd
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.chains import SequentialChain

load_dotenv()

class Oracle:

    post_doc_template= """
    You are a postdoctoral researcher in the field of {category}. You are very knowledgeable and up to date in your research with excellent communication and analytical skills. \
    You can easily synthesize the complex and in depth information to identify how the new body of knowledge could contribute and advance the general research category. \
    You will now read the following research articles, with its associated metadata such as title and author information to assess how these new body of research contributes the research area. \ 
    You will critically evaluate each article and point any fallbacks, and incostincesies as well in comparison the existing literature. \
    You will present your findings in a conscise 300 - 400 word report in way that is understandable by the general audiance who has MBA. \n\n

    {articles}

    """

    business_analyst_template = """
    You are a business analyst in a company's research and development department. The company operates in an area that leverages the academic research from {category}.  \
    You have an MBA from a top-tier school following by several years of industry experience. You have a particular strenght in understanding complex information and  \
    deriving actionable insights optimizing bussiness outcomes. You will read a concise report prepared by a postdoctoral researcher informing you about the recently published research papers by academics. \ 
    You will critically evaluate the information from a strictly business persective, including feasibility of applying these research,  including pros-and cons
    and prepare a brief to the executives identifying, if any how these new research can be applicable in your industry.  \
    You will avoid using first person pronouns, such as I, our, me, my but replace it with third person. For example instead of saying our business model, you need to say the businesses in  working  in {category}  industry.  
    
    \n\n
    
    {postdoc_report}

    """

    def __init__(self, path):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.df = pd.read_csv(path)
        self.llm = ChatOpenAI(openai_api_key = self.api_key, model = "gpt-4", temperature = 0.6)
        self.categories = self.df.category.unique()
        pass

    def ctg_choose(self):
        
        print('for given query papers found it in the following categories:\n')
        for index, item in enumerate(self.categories, start=1):
            print(f"{index}. {item}")

 
        try:
            choice = int(input("\nPlease enter a number corresponding to your choice: "))
            if 1 <= choice <= len(self.categories):
                return self.categories[choice - 1]
            else:
                print("Invalid choice. Please enter a number between 1 and {}.".format(len(self.categories)))
        except ValueError:
            print("Please enter a valid number.")
        
        print(f'You have choosen: {choice}')

        return choice 
        

    def pre_processor(self):
        
        df = self.df.drop(columns=['Unnamed: 0'])
        df['title_author_abstract'] = df.agg('Title is: {0[title]}. Authors are: {0[authors]}. Summary is: {0[summary]}'.format, axis=1 )
        df_grouped = df.groupby('category')['title_author_abstract'].agg('\n__Next Article__: '.join).reset_index()

        ctg = self.ctg_choose()

        articles = ""
        category = ""

        vals = df_grouped.to_dict('records')
        for i in vals:
            if i['category'] == ctg : # change per user input
                category = i['category']
                articles = i['title_author_abstract']

        #return f'Research category is {category}. \n These are the titles, authors, and abstracts of these research articles {articles}:\n'
        return category,articles

    def generator(self):

        postdoc_prompt = ChatPromptTemplate.from_template(self.post_doc_template)

        chain_one = LLMChain(llm=self.llm, prompt=postdoc_prompt, 
                             output_key="postdoc_report"
                            )


        bussines_analyst_prompt = ChatPromptTemplate.from_template(self.business_analyst_template)

        chain_two = LLMChain(llm=self.llm, prompt=bussines_analyst_prompt, 
                             output_key="business_brief"
                            )

        overall_chain = SequentialChain(
            chains=[chain_one, chain_two],
            input_variables=["category","articles"],
            output_variables=["postdoc_report", "business_brief"],
            verbose=True
        )

        docs = self.pre_processor()
        gens = overall_chain({'category':docs[0],'articles':docs[1]})

        
        self.print_report(gens['category'],gens["postdoc_report"],gens['business_brief'])
        
        return gens 


    def print_report(self,category, academic, business):

        print('-' * 80)
        print(f'{" " * 35} REPORT')
        print('-' * 80)

        # Category title
        print(f'{"*" * 5} Category {"*" * 5}')
        print(f'For the chosen category: {category}')
        print()

        # Academic evaluation
        print(f'{"=" * 5} Academic Evaluation {"=" * 5}')
        print(f'This is the critical evaluation from an academic perspective:\n{academic}')
        print()

        # Business evaluation
        print(f'{"+" * 5} Business Evaluation {"+" * 5}')
        print(f'This is the critical evaluation from a business perspective:\n{business}')

        # Report ending
        print('-' * 80)
        print(f'{" " * 28} END OF REPORT')
        print('-' * 80)



