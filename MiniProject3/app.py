import spacy
from wordcloud import WordCloud
import gradio as gr
from spacy.lang.en.stop_words import STOP_WORDS
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")

def wordcloud(text,n):
    def preprocess_text(text):
        # Step 1: Lowercasing
        text = text.lower()

        # Step 2: Removing punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Step 3: Removing stop words
        doc = nlp(text)
        tokens_without_stopwords = [token.text for token in doc if token.text not in STOP_WORDS]

        # Step 4: Handling numbers and symbols (optional)
        # If you want to keep numbers, you can comment out the following line
        tokens_without_stopwords = [token for token in tokens_without_stopwords if not token.isdigit()]

        # Step 5: Text normalization (optional)
        # You can perform stemming or lemmatization here if needed

        return tokens_without_stopwords

    processed_text = preprocess_text(text)
    
    # Step 1: Compute TF-IDF scores
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(processed_text)

    # Step 2: Select top words based on TF-IDF scores
    # Get feature names (words)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Create a dictionary to store word -> tfidf_score pairs
    word_scores = {}
    for i, word in enumerate(feature_names):
        word_scores[word] = tfidf_matrix[:, i].mean()  # Average TF-IDF score for the word

    # Sort the dictionary by TF-IDF scores
    top_words_dict = dict(sorted(word_scores.items(), key=lambda item: item[1], reverse=True))

    # Specify the number of top words to display
    top_n = n

    # Get top n words
    top_n_words_dict = dict(list(top_words_dict.items())[:top_n])

    # Step 3: Generate word cloud
    wordcloud = WordCloud(width=800, height=600, background_color="white")
    wordcloud.generate_from_frequencies(top_n_words_dict)

    # Plot the word cloud
    plt.imshow(wordcloud)
    plt.axis("off")
    
    plt.savefig("plot.png")  # Replace with your desired filename

    return "plot.png"
    
interface = gr.Interface(fn=wordcloud,
                         inputs=[gr.Textbox(label="Job Description", lines=5, placeholder="Paste the Job Description"),
        gr.Slider(minimum=10, maximum=100, label="Scale")],
    outputs="image")
# Launch the interface
interface.launch(inline=False)