# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 14:58:23 2024

@author: TOM
"""

import nest_asyncio
from llama_parse import LlamaParse
import os

nest_asyncio.apply()



##LLAMA PARSE##
llama_parse_document = LlamaParse(api_key = "API_LLAMA_INDEX",result_type = "markdown").load_data("NIPS-2017-attention-is-all-you-need-Paper.pdf")
llama_parse_document[0].text[:100]

##QDRANT##
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import qdrant_client

##FastEmbed##
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings

embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

##Groq##

from llama_index.llms.groq import Groq

llm = Groq(model="mixtral-8x7b-32768", api_key="API_GROQ")
Settings.llm = llm

client = qdrant_client.QdrantClient(api_key="API_QDRANT",url="URL_QDRANT")

vector_store = QdrantVectorStore(client = client, collection_name='qdrant_tom_rag')
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents = llama_parse_document, storage_context=storage_context, show_progress=True)

query_engine = index.as_query_engine()
query = "can you sum up this document ?"
response = query_engine.query(query)
print(response)
