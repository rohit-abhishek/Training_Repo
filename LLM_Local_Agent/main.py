from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# just import the retriever from the vector.py 
from vector import retriever

model=OllamaLLM(model="llama3.2")

template="""
You are an expert in answering questions on Pizza resturant. 

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

# create a prompt using template where reviews and question will be passed
prompt=ChatPromptTemplate.from_template(template)

# allows us to invoke multiple things together and pass to the model
chain=prompt | model

# to test the model quickly run below 
# result=chain.invoke({"reviews" : [] , "question": "What is the best pizza place in town"})
# print(result)

while True:
    print("\n\n-------------------------------------------------------------------")
    question=input("Ask your question (q to quit): ")
    if question=="q":
        break 

    # call retriever to get top 5 reviews and pass it to model along with question 
    reviews=retriever.invoke(question)
    result=chain.invoke({"reviews" : reviews , "question": question})
    print(result)