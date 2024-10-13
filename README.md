# manicod
Source code and dataset for the paper under review

## To run the code

To run try manipulated content detection, you can simply install the requirement packages and run the python script 'llama3_langchain_automatic_from_json_dataset.py'.

The script will be default evaluate the veracity of news headlines from the file 'dataset/final-datasets/news_index_20240724.json'. However, you are free to change it in the python script (line 37).

The LLM adopted by Manicod source code is bosted on Ollama framework using its default local host configuration. You will need to pull the LLM to your local machine and make sure it is set up and runing in the background. Please don't forget to change it in the script (url and port) if you want to use Ollama to access remotely hosted LLMs. You can also change to another LLM by pulling them through Ollama in separate command line/terminal, followed by changing the LLM name in line 33.

# To check the dataset

Please move to the 'dataset' directory and refer to the README file in it.