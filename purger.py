import json

# Open the original file and load the data
with open('Subtask_1_pred.json', 'r') as f:
    data = json.load(f)

# Iterate over all conversations
for conversation in data:
    # Iterate over the 'conversation' list and remove the 'emotion' field
    for utterance in conversation['conversation']:
        if 'emotion' in utterance:
            del utterance['emotion']

    # Remove the 'emotion-cause_pairs' field
    if 'emotion-cause_pairs' in conversation:
        del conversation['emotion-cause_pairs']

# Write the modified data to the new file
with open('prep.json', 'w') as f:
    json.dump(data, f, indent=4)
