import sys
import json

from datetime import datetime

from key import OPENAI_API_KEY
from openai import OpenAI
from config import *


def chat(client: OpenAI, model: str, message: str, system_message: str):
    stream = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': message}, {
            'role': 'system', 'content': system_message}],
        stream=True,
    )

    output_message = ''
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            output_message += chunk.choices[0].delta.content

    return output_message


def run():
    # test run
    client = OpenAI(api_key=OPENAI_API_KEY)

    # set up
    files = [
        '../data/fake_news_context_20240724.json',
        '../data/news_index_20240724.json',
        '../data/fake_news_negation_20240724.json',
    ]

    now = datetime.now()
    cur_time = now.strftime("%m-%d-%H-%M-%S")
    output_suffix = f'{cur_time}.log'

    # pipeline
    for file in files:
        print(f'Start processing {file}')
        # preprocess
        with open(file, 'r') as f:
            data = json.load(f)

        output_file = 'logs/chatgpt_' + file.split('/')[-1] + '_' + output_suffix
        counter = 0
        results = ''

        # retrieve data
        for key in data:
            if counter > ENTRY_PROCESS:
                break

            print(f'Processing {counter}/{ENTRY_PROCESS} ...', end='')
            news = data[key]['text']

            # handle api call
            output_message = chat(client=client, model='gpt-4o-mini',
                                  message=USER_PROMPT.format(statement=news), system_message=SYSTEM_PROMPT)

            # feed back result
            results = results + f'{key}\n\n{news}\n\n{output_message}\n*******************\n'

            counter += 1

            print(f' finished')

        # save results
        print(f'Logs write to {output_file}')
        with open(output_file, 'w') as ofile:
            ofile.write(results)
        
    return 0


def test():
    # test run
    client = OpenAI(api_key=OPENAI_API_KEY)
    output_message = chat(client=client, model='gpt-4o-mini',
                          message='Say this is a test', system_message='')
    print(output_message)


def main():
    run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
