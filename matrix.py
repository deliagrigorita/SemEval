import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Load the data
with open('Subtask_1_pred.json') as f:
    data_pred = json.load(f)
with open('test.json') as f:
    data_test = json.load(f)

# Initialize confusion matrix
confusion_matrix = np.zeros((2, 2))

# Iterate over each conversation
for conv_pred, conv_test in zip(data_pred, data_test):
    # Extract the emotion-cause pairs
    pairs_pred = set(tuple(pair) for pair in conv_pred['emotion-cause_pairs'])
    pairs_test = set(tuple(pair) for pair in conv_test['emotion-cause_pairs'])

    # Calculate the number of matching pairs
    matching_pairs = pairs_pred & pairs_test

    # Calculate the number of overlapping tokens
    tokens_pred = set(range(int(pair[1].split('_')[1]), int(pair[1].split('_')[2])+1) for pair in pairs_pred)
    tokens_test = set(range(int(pair[1].split('_')[1]), int(pair[1].split('_')[2])+1) for pair in pairs_test)
    overlapping_tokens = tokens_pred & tokens_test

    # Update confusion matrix
    confusion_matrix[0, 0] += len(matching_pairs)
    confusion_matrix[0, 1] += len(pairs_pred) - len(matching_pairs)
    confusion_matrix[1, 0] += len(overlapping_tokens)
    confusion_matrix[1, 1] += len(tokens_pred) - len(overlapping_tokens)

# Plot confusion matrix
fig, ax = plt.subplots()
im = ax.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
ax.figure.colorbar(im, ax=ax)
ax.set(xticks=np.arange(confusion_matrix.shape[1]),
       yticks=np.arange(confusion_matrix.shape[0]),
       xticklabels=['Match', 'No Match'], 
       yticklabels=['Pairs', 'Tokens'],
       title='Confusion Matrix',
       ylabel='True label',
       xlabel='Predicted label')

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

fig.tight_layout()
plt.show()
