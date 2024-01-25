import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

with open('train.json', 'r') as f:
    train_data = json.load(f)

utterances = []
labels = []
for convo in train_data:
    for utterance in convo['conversation']:
        for pair in convo['emotion-cause_pairs']:
            if int(pair[0].split('_')[0]) == utterance['utterance_ID']:
                utterances.append(utterance['text'])
                labels.append(pair[0].split('_')[1])

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(utterances)
y_train = labels

model = MultinomialNB()
model.fit(X_train, y_train)

with open('evaluation_data.json', 'r') as f:
    trial_data = json.load(f)

def is_emotion_cause_pair(prev_emotion, curr_emotion, prev_text, curr_text, prev_speaker, curr_speaker):
    rules = [
        {"emotion": "surprise", "previous_emotion": "sadness", "text": "how"},
        {"emotion": "sadness", "text": "sorry", "previous_emotion": "sadness"},
        {"current_speaker_different": True, "text": "?"},
        {"current_speaker_same": True, "text": "?"},
        {"emotion": "surprise", "previous_emotion": "neutral", "text": "what"},
        {"text": "!", "previous_emotion": "neutral"},
        {"text": "well", "previous_emotion": "surprise"},
        {"text": "sorry", "previous_emotion": "neutral"},
        {"text": "huh ? !", "current_speaker_different": True},
        {"text": "why", "previous_emotion": "neutral"},
        {"emotion": "anger", "previous_emotion": "disgust", "text": "hey"},
        {"emotion": "anger", "text": "hey", "previous_emotion": "disgust"},
        {"current_speaker_different": True, "text": "hey"},
        {"current_speaker_same": True, "text": "hey"},
        {"emotion": "anger", "previous_emotion": "neutral", "text": "yeah"},
        {"emotion": "anger", "previous_emotion": "neutral"},
        {"emotion": "anger", "text": "yeah", "previous_emotion": "neutral"},
        {"current_speaker_different": True, "text": "yeah"},
        {"current_speaker_same": True, "text": "yeah"},
        {"emotion": "disgust", "previous_emotion": "neutral", "text": "yeah"},
        {"emotion": "disgust", "previous_emotion": "surprise", "text": "eww"},
        {"emotion": "disgust", "text": "eww", "previous_emotion": "surprise"},
        {"current_speaker_different": True, "text": "eww"},
        {"current_speaker_same": True, "text": "eww"},
        {"emotion": "disgust", "previous_emotion": "disgust", "text": "disgusting"},
        {"emotion": "disgust", "text": "disgusting", "previous_emotion": "disgust"},
        {"current_speaker_different": True, "text": "disgusting"},
        {"current_speaker_same": True, "text": "disgusting"},
        {"emotion": "anger", "previous_emotion": "neutral", "text_is_upper": True},
        {"emotion": "anger", "previous_emotion": "neutral", "text_is_upper": True},
        {"current_speaker_different": True, "text_is_upper": True},
        {"current_speaker_same": True, "text_is_upper": True},
        {"emotion": "anger", "previous_emotion": "joy", "text": "shut up"},
        {"emotion": "anger", "text": "shut up", "previous_emotion": "joy"},
        {"current_speaker_different": True, "text": "shut up"},
        {"current_speaker_same": True, "text": "shut up"},
        {"emotion": "anger", "previous_emotion": "neutral", "text": "..."},
        {"emotion": "anger", "text": "...", "previous_emotion": "neutral"},
        {"emotion": "disgust", "previous_emotion": "neutral", "text": "..."},
        {"emotion": "anger", "previous_emotion": "surprise", "text": "no"},
        {"emotion": "anger", "text": "no", "previous_emotion": "surprise"},
        {"current_speaker_different": True, "text": "no"},
        {"current_speaker_same": True, "text": "no"},
        {"emotion": "fear", "text": "get kinda freaked out"},
        {"emotion": "joy", "previous_emotion": "fear", "text": "freaked out"},
        {"emotion": "joy", "text": "thank you", "previous_emotion": "fear"},
        {"emotion": "joy", "text": "hate", "previous_emotion": "fear"},
        {"emotion": "joy", "text": "oh, god", "previous_emotion": "fear"}
        
        
        #~350 rules
    ]
    for rule in rules:
        if rule.get('emotion') == curr_emotion:
            if 'text' in rule:
                rule_tokens = rule['text'].split()
                input_tokens = curr_text.split()
                if contains_sublist(input_tokens, rule_tokens):
                    start_token = input_tokens.index(rule_tokens[0])
                    end_token = start_token + len(rule_tokens) - 1
                    return True, start_token, end_token
            elif 'current_speaker_different' in rule and rule['current_speaker_different'] and prev_speaker != curr_speaker:
                tokens = curr_text.split()
                return True, 0, len(tokens) - 1
            elif 'current_speaker_same' in rule and rule['current_speaker_same'] and prev_speaker == curr_speaker:
                tokens = curr_text.split()
                return True, 0, len(tokens) - 1
            elif 'text_is_upper' in rule and rule['text_is_upper'] and curr_text.isupper():
                tokens = curr_text.split()
                upper_tokens = [token for token in tokens if token.isupper()]
                start_token = tokens.index(upper_tokens[0])
                end_token = tokens.index(upper_tokens[-1])
                return True, start_token, end_token
            elif 'current_speaker' in rule and rule['current_speaker'] == curr_speaker:
                tokens = curr_text.split()
                return True, 0, len(tokens) - 1
    return False, None, None

def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in range(len(lst)-n+1))

def generate_json(conversation):
    emotion_cause_pairs = set()
    for i in range(len(conversation['conversation'])):
        for j in range(i+1, len(conversation['conversation'])):
            prev_utterance = conversation['conversation'][i]
            curr_utterance = conversation['conversation'][j]
            X_test_prev = vectorizer.transform([prev_utterance['text']])
            X_test_curr = vectorizer.transform([curr_utterance['text']])
            prev_emotion = model.predict(X_test_prev)[0]
            curr_emotion = model.predict(X_test_curr)[0]
            is_pair, start, end = is_emotion_cause_pair(prev_emotion, curr_emotion, prev_utterance['text'], curr_utterance['text'], prev_utterance['speaker'], curr_utterance['speaker'])
            if is_pair:
                cause = f"{j+1}_{start}_{end}"
                pair = (f"{j+1}_{curr_emotion}", cause)
                emotion_cause_pairs.add(pair)
                tokens = curr_utterance['text'].split()
                emotion_cause_pairs.add((f"{i+1}_{prev_emotion}", f"{j+1}_{0}_{len(tokens) - 1}"))

    json_data = {
        "conversation_ID": conversation['conversation_ID'],
        "conversation": conversation['conversation'],
        "emotion-cause_pairs": list(emotion_cause_pairs)
    }

    return json_data

json_data = [generate_json(conversation) for conversation in trial_data]

with open('Subtask_1_pred.json', 'w') as f:
    json.dump(json_data, f, indent=4)


def generate_emotions_list(conversations):
    emotions_list = []
    for conversation in conversations:
        for utterance in conversation['conversation']:
            X_test = vectorizer.transform([utterance['text']])
            emotion = model.predict(X_test)[0]
            emotions_list.append({
                'utterance_ID': utterance['utterance_ID'],
                'text': utterance['text'],
                'emotion': emotion
            })

    with open('emotions-list.json', 'w') as f:
        json.dump(emotions_list, f, indent=4)

generate_emotions_list(trial_data)