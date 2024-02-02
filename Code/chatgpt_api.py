import pandas as pd
from openai import OpenAI
from drug_groups_with_comments import *
from unclassified_drugs import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

client = OpenAI(
    # This is the default and can be omitted
    api_key="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"
)


medicine_groups = list(di.keys())


di = {}
for medicine in unclassified:
    # medicine = 'lalal'
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Can you classify {medicine} into one of the following categories: {medicine_groups}. "
                           f"If it isn't possible, say that it is unclassified.",
            }
        ],
        model="gpt-3.5-turbo",
    )
    reply = chat_completion.choices[0].message.content
    di[medicine] = reply


df = pd.DataFrame.from_dict(di, orient='index')


new_di = {}
for drug in df.index:
    # chat_reply = df.loc['estrogen']
    chat_reply = df.loc[drug].reset_index(drop=True)[0]
    group_li = []
    for drug_group in medicine_groups:
        if drug_group in chat_reply:
            group_li.append(drug_group)

    new_di[drug] = group_li


df['group'] = df.index.map(new_di)
df['group_1'] = [i[0] if len(i) > 0 else i for i in df['group']]
df.to_csv('chat_gpt_classified.csv')

