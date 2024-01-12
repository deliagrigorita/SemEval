import json

def apply_rules(previous_speaker, current_speaker, previous_emotion, current_emotion, current_text):

    #surprise and sadness
    if current_emotion == "surprise" and previous_emotion == "sadness" and "how" in current_text.lower():
        return True
    elif current_emotion == "surprise" and previous_emotion == "sadness":
        return True
    #elif current_emotion == "sadness" and "sorry" in current_text.lower() and previous_emotion == "sadness":
        #return True
    elif current_speaker != previous_speaker and "?" in current_text:
        return True
    elif current_speaker == previous_speaker and "?" in current_text:
        return True
    elif current_emotion == "surprise" and previous_emotion == "neutral" and "what" in current_text.lower():
        return True
    elif "!" in current_text and previous_emotion == "neutral":
        return True
    elif "well" in current_text.lower() and previous_emotion == "surprise":
        return True
    elif "sorry" in current_text.lower() and previous_emotion == "neutral":
        return True
    elif "huh ? !" in current_text.lower() and current_speaker != previous_speaker:
        return True
    elif "why" in current_text.lower() and previous_emotion == "neutral":
        return True
    
    #anger and disgust
    elif current_emotion == "anger" and previous_emotion == "disgust" and "hey" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "disgust":
        return True
    elif current_emotion == "anger" and "hey" in current_text.lower() and previous_emotion == "disgust":
        return True
    elif current_speaker != previous_speaker and "hey" in current_text.lower():
        return True
    elif current_speaker == previous_speaker and "hey" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "disgust" and "hey" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral" and "yeah" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral":
        return True
    elif current_emotion == "anger" and "yeah" in current_text.lower() and previous_emotion == "neutral":
        return True
    elif current_speaker != previous_speaker and "yeah" in current_text.lower():
        return True
    elif current_speaker == previous_speaker and "yeah" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "neutral" and "yeah" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "surprise" and "eww" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "surprise":
        return True
    elif current_emotion == "disgust" and "eww" in current_text.lower() and previous_emotion == "surprise":
        return True
    elif current_speaker != previous_speaker and "eww" in current_text.lower():
        return True
    elif current_speaker == previous_speaker and "eww" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "surprise" and "eww" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "disgust" and "disgusting" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "disgust":
        return True
    elif current_emotion == "disgust" and "disgusting" in current_text.lower() and previous_emotion == "disgust":
        return True
    elif current_speaker != previous_speaker and "disgusting" in current_text.lower():
        return True
    elif current_speaker == previous_speaker and "disgusting" in current_text.lower():
        return True
    elif current_emotion == "disgust" and previous_emotion == "disgust" and "disgusting" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral" and current_text.isupper():
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral":
        return True
    elif current_emotion == "anger" and current_text.isupper() and previous_emotion == "neutral":
        return True
    elif current_speaker != previous_speaker and current_text.isupper():
        return True
    elif current_speaker == previous_speaker and current_text.isupper():
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral" and current_text.isupper():
        return True
    elif current_emotion == "anger" and previous_emotion == "joy" and "shut up" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "joy":
        return True
    elif current_emotion == "anger" and "shut up" in current_text.lower() and previous_emotion == "joy":
        return True
    elif current_speaker != previous_speaker and "shut up" in current_text.lower():
        return True
    elif current_speaker == previous_speaker and "shut up" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "joy" and "shut up" in current_text.lower():
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral" and "..." in current_text:
        return True
    elif current_emotion == "anger" and previous_emotion == "neutral":
        return True
    elif current_emotion == "anger" and "..." in current_text and previous_emotion == "neutral":
        return True
    #elif current_speaker != previous_speaker and "..." in current_text:
        #return True
   #elif current_speaker == previous_speaker and "..." in current_text:
        #return True
    elif current_emotion == "disgust" and previous_emotion == "neutral" and "..." in current_text:
        return True 
    elif current_emotion == "anger" and previous_emotion == "surprise" and "no" in current_text:
        return True
    elif current_emotion == "anger" and previous_emotion == "surprise":
        return True
    elif current_emotion == "anger" and "no" in current_text and previous_emotion == "surprise":
        return True
    elif current_speaker != previous_speaker and "no" in current_text:
        return True
    elif current_speaker == previous_speaker and "no" in current_text:
        return True
    elif current_emotion == "anger" and previous_emotion == "surprise" and "no" in current_text:
        return True
  
    #joy and fear
    elif current_emotion == "fear" and "get kinda freaked out" in current_text.lower():
        return True
    elif current_emotion == "sadness" and previous_emotion == "fear":
        return True
    elif current_emotion == "neutral" and previous_emotion == "sadness":
        return True
    elif current_speaker == "fear" and previous_emotion == "neutral":
        return True
    elif current_speaker == "joy" and previous_emotion == "fear":
        return True
    elif current_emotion == "joy" and previous_emotion == "fear" and "freaked out" in current_text.lower():
        return True
    elif current_emotion == "joy" and previous_emotion == "fear":
        return True
    elif current_emotion == "joy" and "thank you" in current_text.lower() and previous_emotion == "fear":
        return True
    elif current_emotion == "joy" and "hate" in current_text.lower() and previous_emotion == "fear":
        return True
    elif current_emotion == "joy" and "oh, god" in current_text.lower() and previous_emotion == "fear":
        return True

    #end
    else:
        return False


def generate_utterance_pairs(conversation):
    utterance_pairs = []

    for i in range(len(conversation)):
        for j in range(len(conversation)):
            pair = (conversation[i]["utterance_ID"], conversation[j]["utterance_ID"])
            yes_or_no = "yes" if apply_rules(conversation[i]["speaker"],
                                             conversation[j]["speaker"],
                                             conversation[i].get("emotion", ""),
                                             conversation[j].get("emotion", ""),
                                             conversation[j]["text"]) else "no"
            if yes_or_no == "yes":
                tokens_i = conversation[i]['text'].split()
                tokens_j = conversation[j]['text'].split()
                if conversation[i]['text'] in conversation[j]['text']:
                    start_index = tokens_j.index(tokens_i[0])
                    end_index = start_index + len(tokens_i) - 1
                    pair_result = [f"{i}_{conversation[i].get('emotion', '')}", f"{j}_{start_index}_{end_index}"]
                    utterance_pairs.append(pair_result)
                    print(f"{pair_result}")

    return utterance_pairs



conversation_data = {
    #start of the conversation data (the one below is just an example provided, insert whatever conversation you intend to analyse)
        "conversation_ID": 4,
        "conversation": [
            {
                "utterance_ID": 1,
                "text": "Barry , I am sorry ...",
                "speaker": "Rachel",
                "emotion": "sadness"
            },
            {
                "utterance_ID": 2,
                "text": "I am so sorry ...",
                "speaker": "Rachel",
                "emotion": "sadness"
            },
            {
                "utterance_ID": 3,
                "text": "I know you probably think that this is all about what I said the other day about you making love with your socks on , but it is not ... it is not , it is about me , and I ju ...",
                "speaker": "Rachel",
                "emotion": "sadness"
            }
        ],  
    #end of the conversation data
}

utterance_pairs = generate_utterance_pairs(conversation_data["conversation"])

conversation_data["emotion-cause_pairs"] = utterance_pairs

# Save the conversation data to a JSON file
with open('conversation_data.json', 'w') as json_file:
    json.dump(conversation_data, json_file)