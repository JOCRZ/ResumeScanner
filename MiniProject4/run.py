import spacy

# insert job description
job_description = """
We are seeking a talented and experienced Data Scientist to join our team. As a Data Scientist, you will be responsible for analyzing complex data, developing advanced models, and driving data-driven strategies to solve business problems. You will work closely with cross-functional teams to extract insights, build predictive models, and support decision-making processes.

Responsibilities

Apply advanced analytics techniques to extract actionable insights from large and complex datasets

Develop machine learning models and algorithms to solve business problems and optimize performance

Collaborate with cross-functional teams to identify opportunities for data-driven solutions

Clean, analyze, and visualize data to drive key insights and trends

Conduct statistical analysis and hypothesis testing to validate models and results

Improve data quality and integrity through data cleaning and validation procedures

Communicate findings and recommendations to both technical and non-technical stakeholders clearly and concisely

Requirements

Bachelor's degree in Data Science, Computer Science, Statistics, or a related field

Experience Preferred:0-3 years

Proficient in programming languages such as Python and R

Strong analytical and problem-solving skills

Knowledge of data visualization tools, such as Tableau or Power BI

Familiarity with big data technologies, such as Hadoop and Spark, is a plus

Excellent communication and presentation skills, with the ability to convey complex concepts to a diverse audience
"""


ner_model_path = r"models/model-best"

ner_model = spacy.load(ner_model_path)

# test the algorithm
doc = ner_model(job_description)

for ent in doc.ents:
    print(ent.text, '--->', ent.label_)