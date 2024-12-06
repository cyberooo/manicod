## Model Selection

*Manicod* does not rely on LLM’s knowledge to determine the veracity but instead resorts to the natural language comprehension capabilities to perform knowledge-grounded inference. 
Before deciding to use Llama 3.1, we performed a round of preliminary studies on a smaller scale to compare the performance of different LLMs (with similar sizes). 
Specifically, we evaluated the performance of four LLMs -- llama3.1:8b-instruct, llama3:8b-instruct, gemma:7b, mistral:7b, using the LangChain RAG technique on data collected on Aug 11. The comparison of overall performance is shown below.

| Models     | llama3.1:8b | llama3:8b | gemma:7b | mistral:7b |
| ---------- | -------- | ------- | -------- | ------ |
| Precision  | **0.846** | 0.776 | 0.698 | 0.775 |
| Recall     | 0.941 | 0.930 | 0.842 | **0.980** |
| Accuracy   | **0.891** | 0.846 | 0.764 | 0.865 |
| F1 score   | **0.852** | 0.779 | 0.696 | 0.797 | 

We observed that the four evaluated LLMs performed similarly, and we chose the Llama 3.1 in the paper for its best overall performance.  Besides this, the results also reveal that the detection of *Manicod* mainly relies on the natural language comprehension capabilities of LLMs rather than their intrinsic knowledge of recent events. 

> We have also attempted to perform the knowledge-grounded inference on larger models, e.g., 70b version of Llama3, and observed very limited improvement with significant computation resource usage and time sacrifice. Therefore, we adopt Llama 3.1 (8b) to balance the performance and cost of time and hardware resources.
