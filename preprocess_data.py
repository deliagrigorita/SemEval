import json
from transformers import BertTokenizer

def preprocess_data(input_data, output_file):  #Def o funcție numita "preprocess_data" care primeste 2 argumente: input_data - datele de intrare (o lista de conversatii in format JSON) si output_file - calea catre fisierul in care vor fi salvate datele preprocesate
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') #Initializeaza un obiect tokenizer folosind modelul BERT de lb eng (bert-base-uncased) (tokenizarea textului)

    pairs = [] #Initializeaza o lista goala pentru a stoca perechile de date preprocesate

    for conversation_data in input_data: #Itereaza prin fiecare conversatie din input_data
        conversation_id = conversation_data["conversation_ID"]  # Extrage ID-ul conversatiei curente
        utterances = conversation_data["conversation"] #Extrage lista de replici (utterances) din conversatia curenta

        for i, utterance in enumerate(utterances): #Itereaza prin fiecare replica din conversatie, tinand cont si de indexul replicii (i)- variabila i reprezintă indexul replicii curente în timpul iteratiei
            emotion = utterance.get("emotion") #Extrage emotia din replica, daca exista
            if emotion and emotion.lower() in ['anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise']: #Verifica daca emotia este valida si se afla in lista data de emotii. Daca da, continua cu procesarea replicii
                emotion_category = emotion.lower() #Stocheaza categoria emotionala ( ca litere mici)
                emotion_id = f"{i + 1}_{emotion_category}" #Constr. un ID unic pentru replica, utilizand indexul si categoria emotionala

                # Tokenizeaza textul replicii cu ajutorul obiectului tokenizer si obtine tensori de PyTorch
                emotion_tokenized = tokenizer(utterance["text"], return_tensors="pt")

           
                emotion_input_ids = emotion_tokenized["input_ids"].tolist() #Extrage identificatorii tokenilor (input_ids) sub forma de lista
                emotion_attention_mask = emotion_tokenized["attention_mask"].tolist() #In procesul de tokenizare, fiecare cuvant a textului original este transformata intr-un set de identificatori de tokeni
                
                #attention_mask este un vector binar care indica care dintre acesti tokeni sunt cu adevarat tokeni semnificativi si care sunt tokeni de umplutura (0 si 1)

                for j in range(i + 1, len(utterances)): # Itereaza prin replicile urmatoare pentru a identifica cauzele asociate cu emotiile
                    cause_text = utterances[j]['text'] #Extrage textul cauzei din replicile ulterioare
                    cause_id = f"{j + 1}_{cause_text}" #Construieste un ID unic pentru cauza

                    #Tokenizează textul cauzei si obtine tensori de PyTorch
                    cause_tokenized = tokenizer(cause_text, return_tensors="pt")

                    #Extrage identificatorii tokenilor pentru cauza sub forma de lista
                    cause_input_ids = cause_tokenized["input_ids"].tolist()
                    cause_attention_mask = cause_tokenized["attention_mask"].tolist()
                    
                    #Adauga perechea de date preprocesate la lista pairs:
                    pairs.append({
                        "emotion_id": emotion_id,
                        "emotion_category": emotion_category,
                        "emotion_input_ids": emotion_input_ids,
                        "emotion_attention_mask": emotion_attention_mask,
                        "cause_id": cause_id,
                        "cause_input_ids": cause_input_ids,
                        "cause_attention_mask": cause_attention_mask
                    })

    if pairs: # Verifica daca lista pairs nu este goala
        # Salveaza lista de perechi ca un singur fisier JSON
        with open(output_file, 'w') as f:
            json.dump(pairs, f, indent=2)

if __name__ == "__main__":
    input_file_path = "C:\\Users\\40736\\OneDrive\\Desktop\\SemEval\\Subtask_1_train.json"

    output_file_path = "output_file.json"

    with open(input_file_path, 'r') as input_file:
        input_data = json.load(input_file) # incarc datele JSON intr-o variabila "input_data"

    preprocess_data(input_data, output_file_path) #Apelul functiei preprocess_data pentru prelucrarea datelor si salvarea rezultatelor in fisierul de iesire

#"cauză" se refera la replicile ulterioare dintr-o conversatie