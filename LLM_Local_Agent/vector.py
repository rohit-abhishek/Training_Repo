from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os 
import pandas as pd

# read the CSV 
df=pd.read_csv("data/realistic_restaurant_reviews.csv")

# create embeddings object 
emnbeddings=OllamaEmbeddings(model="mxbai-embed-large")

# create location to store the chorma database 
db_location="store/chroma_langchain_db"
add_documents=not os.path.exists(db_location)

print (add_documents)

if add_documents:
    documents=[] 
    ids=[] 

    for i, row in df.iterrows():
        document=Document(page_content=row["Title"] + " " + row["Review"],                            # page_content is the data which we want to query the database (result set. In this example it is Title and Review)
            metadata={"rating": row["Rating"], "date": row["Date"]},                                  # Is the additional data passed to the model - but not used to query the database 
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)


# Add these information to vector store 
vector_store=Chroma(
    collection_name="resturant_reviews", 
    persist_directory=db_location,
    embedding_function=emnbeddings
)

# create the vector store 
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)


# make this vector store usable to LLM 
retriever=vector_store.as_retriever(
    search_kwargs={"k": 5}                                                                              # Grab 5 reviews from the vector and provide the response
)

