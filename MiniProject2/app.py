import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('data_Merademy_2024-02-11_to_2024-02-18.csv')

## Drop rows with NaN values in the 'message' column
df.dropna(subset=['message'], inplace=True)
df['message'] = df['message'].str.lower()

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Fit and transform the 'message' column after replacing NaN with empty strings
tfidf_matrix = tfidf_vectorizer.fit_transform(df['message'].fillna(''))

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)




def get_similar_jobs(job_title, cosine_sim=cosine_sim, df=df):
    # Check if there are any rows containing the specified job title
    if df['message'].str.contains(job_title).any():
        # Get the index of the job title
        idx = df[df['message'].str.contains(job_title)].index[0]

        # Get similarity scores of the job with all other jobs
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the jobs based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the top 5 similar jobs
        sim_scores = sim_scores[1:6]

        # Get the job indices
        job_indices = [i[0] for i in sim_scores]

        # Return the similar job titles
        return df['message'].iloc[job_indices]
    else:
        return "No similar job titles found."


def main():
    st.title("Job Hunt Search")
    
    # Job title search input
    job_title = st.text_input("Enter a job title:", "")
    
    if st.button("Search"):
        if job_title:
            similar_jobs = get_similar_jobs(job_title)
            st.write(similar_jobs)
        else:
            st.write("Please enter a job title.")
            
if __name__ == "__main__":
    main()
