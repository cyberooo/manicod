# Baseline bechmarking

"baseline_benchmarking_fact_checking.py" is for the benchmarking of COVID and FEVER tasks. Since the claims in these two datasets are easy to be verified thorugh Internet, we run them in the same way of what Manicod does.

"baseline_benchmarking_claim_verification.py" is for the tasks that we mock the online retrieval by directly using the supporting documents/evidence provided in the dataset. In other words, the Google search API is not used in this script.

The folder "ablation-chatgpt" is for ablation study that we run the exactly same manipulated content dataset on ChatGPT 4o mini. For ablation study runing the Llama 3.1 model, we use the normal Manifod script by manually commenting out the RAG code. No separate code is needed for Llama 3.1 ablation study.