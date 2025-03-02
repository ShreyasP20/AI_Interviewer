import nltk 
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
current_answer= "Python is my main language"
ideal_nu_answer = "I am proficient in Python Language"
tokens1 = set(word_tokenize(current_answer.lower())) - set(stopwords.words('english'))
tokens2 = set(word_tokenize(ideal_nu_answer.lower())) - set(stopwords.words('english'))
similarity_score = len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))
if similarity_score < 50:
    follow_up_q = True
    print("Follow Up question to be asked"+ similarity_score)
else:
    follow_up_q = False
    print(" No Follow Up question to be asked"+ similarity_score)
