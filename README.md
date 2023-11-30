# Textual Emotion-Cause Pair Extraction in Conversations

### Extracting all emotion-cause pairs from the given conversation ("Friends" tv series) solely based on text, where the emotion cause is defined and annotated as a textual span.

<img width="1070" alt="image" src="https://github.com/deliagrigorita/SemEval/assets/79158831/f9044086-da47-4470-b51b-ac297886aa67">




#### Input: a conversation containing the speaker and the text of each utterance

#### Output: all emotion-cause pairs, where each pair contains an emotion utterance along with its emotion category and the textual cause span in a specific cause utterance, e.g., (3_joy, 2_You made up!). The emotion category should be one of Ekman’s six basic emotions including Anger, Disgust, Fear, Joy, Sadness and Surprise. 

*Note: There may be multiple cause spans corresponding to the same emotion, thus forming multiple pairs.*

Task example:
```
{
"conversation_ID": 5,
"conversation": [
	{
		"utterance_ID": 1,
		"text": "Oh , look , wish me luck !",
		"speaker": "Rachel",
		"emotion": "joy"
	},
	{
		"utterance_ID": 2,
		"text": "What for ?",
		"speaker": "Monica",
		"emotion": "neutral"
	},
	{
		"utterance_ID": 3,
		"text": "I am gonna go get one of those job things .",
		"speaker": "Rachel",
		"emotion": "joy"
	}
	],
"emotion-cause_pairs": [
	[
		"1_joy",
		"3_I am gonna go get one of those job things ."
	],
	[
		"3_joy",
		"3_I am gonna go get one of those job things ."
	]
	]
}
```
