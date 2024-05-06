
import os
import argparse

import llama_index
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="create and save files embedding to vector store."
    )

    parser.add_argument(
        "-persist_dir",
        type=str,
        default='persist_dir',
        help="dir",
    )

    return parser.parse_args()


def get_openai_api_key():
    if 'OPENAI_API_KEY' in os.environ:
        key = os.environ.get('OPENAI_API_KEY')
    else:
        if os.path.exists('openai_api_key.txt'):
            with open('openai_api_key.txt', 'r') as f:
                key = f.read().strip()
                if key == '':
                    raise ValueError("openai_api_key.txt is empty")
        else:
            raise ValueError("openai_api_key.txt or OPENAI_API_KEY not found")
    print('API key found')
    return key
            

def create_vector_store_index(api_key):
    NODE_PARSER_CHUNK_SIZE = 512
    NODE_PARSER_CHUNK_OVERLAP = 10
    preprocessed_dir = 'preprocessed'

    embed_llm = OpenAIEmbedding(temperature=0, model="text-embedding-3-small", api_key=api_key)
    node_parser = SentenceSplitter.from_defaults(
        chunk_size=NODE_PARSER_CHUNK_SIZE,
        chunk_overlap=NODE_PARSER_CHUNK_OVERLAP,
        # callback_manager=callback_manager,
    )
    # db = chromadb.PersistentClient(path="./chroma_db")
    # chroma_collection = db.get_or_create_collection("quickstart")
    # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    # storage_context = StorageContext.from_defaults(vector_store=vector_store)

    Settings.embed_model = embed_llm
    Settings.node_parser = node_parser
    # Settings.vector_store = vector_store
    # Settings.storage_context  = storage_context

    documents = SimpleDirectoryReader(preprocessed_dir).load_data()

    print("Creating index...")
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_llm,
    )
    print("Index created.")
    
    return index

def save_vector_store_index(index, persist_dir="persist_dir"):
    index.storage_context.persist(persist_dir=persist_dir)

def vdb(persist_dir="persist_dir"):
    api_key = get_openai_api_key()
    index = create_vector_store_index(api_key=api_key)
    save_vector_store_index(index, persist_dir=persist_dir)

if __name__ == '__main__':
    args = parse_args()

    vdb(args.persist_dir)