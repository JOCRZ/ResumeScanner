from gradio import Interface, Text, Dropdown, Number
import spacy
from collections import Counter


nlp = spacy.load("en_core_web_sm")


def phrase_counter(text, gram, freq):
    doc = nlp(text)
    count = freq
    
    if gram == 'unigram':
        unigram_freq = Counter()
        for token in doc:
            unigram_freq[token.text] += 1

        return {k: v for k, v in unigram_freq.items() if v > count}

    elif gram == 'bigram':
        bigram_freq = Counter()
        for i in range(len(doc) - 1):
            bigram = (doc[i].text, doc[i + 1].text)
            bigram_freq[bigram] += 1

        return {k: v for k, v in bigram_freq.items() if v > count}

    elif gram == 'trigram':
        trigram_freq = Counter()
        for i in range(len(doc) - 2):
            trigram = (doc[i].text, doc[i + 1].text, doc[i + 2].text)
            trigram_freq[trigram] += 1

        return {k: v for k, v in trigram_freq.items() if v > count}

    else:
        return 'Choose from the options'
    


interface = Interface(fn=phrase_counter,
    inputs=[Text(label="Enter Text"), Dropdown(label="Choose Gram", choices=["unigram", "bigram", "trigram"]), Number(label="Frequency")],
    outputs="text"
)

# Launch the interface
interface.launch()

