import pandas as pd

from datasets import load_dataset

ds_lsat = load_dataset("dmayhem93/agieval-lsat-ar")

# for num_tokens in [512, 1024, 2048, 3600, 4096, 8192, 16384, 32768]:
for num_tokens in [-512, -1024, -2048, -3600, -4096, -8192]:
# for num_tokens in [128, 256]:
# for num_tokens in [4000]:
# for num_tokens in [-1]:
    # for num_tokens in [32768]:
    # for num_tokens in [-1]:
    all_data = []
    # for i in range(len(ds_lsat['test'])):
    for i in range(len(ds_lsat['test'])):

        # Add Options to the question
        question = ds_lsat['test'][i]['query']
        correct_choice = chr(65 + ds_lsat['test'][i]['gold'][0])
        if num_tokens < -1:
            question = f"{question}"+"\n\nLet's think step by step and output the final answer (eg, A, B, C, D) within \\boxed{}." + (f" Think for maximum {num_tokens} tokens.")
        else:
            question = f"{question}"+"\n\nLet's think step by step and output the final answer (eg, A, B, C, D) within \\boxed{}." + (f" Think for {num_tokens} tokens." if num_tokens != -1 else "")
        print(question)
        print(correct_choice)

        all_data.append({
                    "data_source": "gpqa",
                    "prompt": [{
                        "role": "user",
                        "content": question
                    }],
                    "ability": "math",
                    "reward_model": {
                        "style": "rule",
                        "ground_truth": correct_choice,
                        "num_tokens": num_tokens
                    },
                    "extra_info": {
                        'split': 'test',
                        'index': i
                    }
                })
    if num_tokens != -1:
        if num_tokens < -1:
            pd.DataFrame(all_data).to_parquet(f'~/deepscaler/data9_{num_tokens}/lsat.parquet')
        else:
            pd.DataFrame(all_data).to_parquet(f'~/deepscaler/data_{num_tokens}/lsat.parquet')
    else:
        pd.DataFrame(all_data).to_parquet(f'~/deepscaler/data/lsat.parquet')
    