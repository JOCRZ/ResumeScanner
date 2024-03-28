import gradio as gr
import spacy
import re



# removing formatting

def remove_formatting(text):
    # Remove bold formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    
    # Remove italic formatting
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Remove underline formatting
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # Add more patterns for other formatting styles as needed
    
    return text

# lower casing 
def convert_to_lowercase(text):
   
    text = text.lower()
    return text


# removing punctuation

def remove_punctuation(text):
    # Define a regular expression pattern to match punctuation marks
    punctuation_pattern = r'[^\w\s,]' # Matches any character that is not a word character or whitespace
    
    # Use the sub() function from the re module to replace punctuation marks with an empty string
    text = re.sub(punctuation_pattern, '', text)
    
    return text


# removing white spaces

def remove_whitespace(text):
    # Define a regular expression pattern to match whitespace characters
    whitespace_pattern = r'\s+'
    
    # Use the sub() function from the re module to replace whitespace characters with an empty string
    text = re.sub(whitespace_pattern, '', text)
    
    return text


# removing stop words

nlp = spacy.load("en_core_web_sm")

def remove_stopwords_spacy(text):
    doc = nlp(text)
    filtered_tokens = [token.text for token in doc if not token.is_stop]
    text = ' '.join(filtered_tokens)
    return text 


def preprocessing_text(text):

    text1 = remove_formatting(text)
    text2 = convert_to_lowercase(text1)
    text3 = remove_punctuation(text2)
    text4 = correct_spelling_spellchecker(text3)
    #text5 = remove_whitespace(text4)
    text6 = remove_stopwords_spacy(text4)

    return text6


interface = gr.Interface(fn=preprocessing_text,inputs='text',outputs='text')

interface.launch()