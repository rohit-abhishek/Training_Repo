# running local LLM - ollama 


On terminal type command - 
    $ ollama list -> Get the list of all LLMs currently installed 

Run llama2 - 
    $ ollama run llama 

You can see ollama icon on task bar. By default ollama exposes all the API endpoints when runing. You can either close using the icon and issue following command on terminal. By default it runs on localhost, port 11434
    $ ollama serve 

Once the llama model is up and running. You can run work_with_local_llm_requests.py to stream the response from LLM using requests package.
You can also use work_with_local_llm_client.py as well which is making use of ollama package. 

# Customization of LLMs
In the current workspace, there is a directory file called - Modelfile - this contains some of the customization to Ollama models. 
You need this file to create your own model using command below from the current workspace directory - 
    $ ollama create <new name of the model> -f Modelfile

You can issue below command to see your new model 
    $ ollama list


