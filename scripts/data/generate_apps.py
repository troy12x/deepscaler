import pandas as pd

from datasets import load_dataset

ds = load_dataset("codeparrot/apps", "competition")

# for num_tokens in [512, 1024, 2048, 3600, 4096, 8192, 16384, 32768]:
# for num_tokens in [128, 256]:
# for num_tokens in [4000]:
for num_tokens in [-1]:
    all_data = []
    for i in range(len(ds['test'])):

        # Add Options to the question
        question = ds['test'][i]['question']
        question = f"Write a program in python to solve the following problem: {question}"+"\n\nLet's think step by step and output the final python program in the following format: ```\n<python code>\n```" + (f" Think for {num_tokens} tokens." if num_tokens != -1 else "")

        all_data.append({
                    "data_source": "gpqa",
                    "prompt": [{
                        "role": "user",
                        "content": question
                    }],
                    "ability": "math",
                    "reward_model": {
                        "style": "rule",
                        "ground_truth": ds['test'][i]['solutions'],
                        "num_tokens": num_tokens
                    },
                    "extra_info": {
                        'split': 'test',
                        'index': i,
                        'problem_id' : ds['test'][i]['problem_id'],
                        'difficulty' : ds['test'][i]['difficulty']
                    }
                })
    if num_tokens != -1:
        pd.DataFrame(all_data).to_parquet(f'~/deepscaler/data_{num_tokens}/apps.parquet')
    else:
        pd.DataFrame(all_data).to_parquet(f'~/deepscaler/data/apps.parquet')
    