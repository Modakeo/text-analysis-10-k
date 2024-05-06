from llama_index.llms.openai import OpenAI
import re
import embedding
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core import get_response_synthesizer


SYSTEM_MESSAGE = """
    You are an expert financial analyst that always answers questions with the most relevant information using the tools at your disposal.
    These tools have information regarding companies that the user has expressed interest in.
    Here are some guidelines that you must follow:
    * For financial questions, you must use the tools to find the answer and then write a response.
    * Even if it seems like your tools won't be able to answer the question, you must still use them to find the most relevant information and insights. Not using them will appear as if you are not doing your job.
    * You may assume that the users financial questions are related to the documents they've selected.
    * For any user message that isn't related to financial analysis, respectfully decline to respond and suggest that the user ask a relevant question.
    * If your tools are unable to find an answer, you should say that you haven't found an answer but still relay any useful information the tools found.
    """.strip()

TEMPLATE_QUERY = """In the 10-K file of {ticker} {year}, what is {key_fact} for {year}, cite the page number? 
Besides answer in a text format, please prove it in a python number format in a new single line, convert billion. Like 'python: 11.5'
"""

PATTERN = r"python:\s*([\d.]+)"

API_KEY = embedding.get_openai_api_key()


def query_1(query_engine, ticker, year, key_fact):
    local_query = TEMPLATE_QUERY.format(ticker=ticker, year=year, key_fact=key_fact)
    response = query_engine.query(local_query)
    print(response)
    return response


def create_query_engine(index, api_key=API_KEY):
    api_key = embedding.get_openai_api_key()
    llm_base = OpenAI(temperature=0, model="gpt-3.5-turbo-0125", system_prompt=SYSTEM_MESSAGE, api_key=api_key)
    # query_engine = index.as_query_engine(llm=llm_base)

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=20,
    )
    response_synthesizer = get_response_synthesizer(llm=llm_base)
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.5)],
    )

    return query_engine

def loop_query_1(index, ticker, years, key_fact):
    query_engine = create_query_engine(index)
    output = {}
    for year in years:
        print(f"Querying {ticker} {year} {key_fact}...")
        value = find_numbers(query_1(query_engine, ticker, year, key_fact))
        output[year] = value
    return output


def find_numbers(response):
    text = response.response
    match = re.search(PATTERN, text)

    # If a match is found, extract the number
    if match:
        number = match.group(1)
    else:
        number = '0'
        print("No match found")

    return float(number)