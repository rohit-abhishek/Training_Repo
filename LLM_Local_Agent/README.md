# This uses embedding technique. fine tunining requires Google Collab to work with 

Installation - 
    You need langchain, langchain-ollama, and langchain-chorma for this. Install these packages. 
    You will need llama3.2. If not installed issue command 
        $ ollama pull llama3.2 
    You will also need embedding model for this. This embedding model to convert the data to vectors. 
        $ ollama pull mxbai-embed-large 


data folder contains some fake data for resturant. We will create AI agent to get the answer for what we want from this file. 

Source code -
    main.py which takes reviews and prompts user to provide the question. 
    vector.py to vectorize the document

