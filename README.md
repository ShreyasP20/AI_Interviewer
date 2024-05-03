# AIvyinterviewer

AIvyinterviewer is an application designed to prepare users for job interviews by utilizing various AI technologies, particularly Gemini tools. It assists users by taking their job title, extracting their resume either in PDF format or image format, and generating interview questions based on their resume and job title. The application then accepts voice input from the user as answers to the questions, evaluates the similarity between the user's answers and ideal answers generated by Gemini AI, and provides feedback accordingly. It also allows for follow-up questions if needed and stores similarity scores for further analysis.

## Features

- Takes user's job title and resume input (PDF or image).
- Extracts text from PDF resumes using PyPDF.
- Processes image resumes using Gemini API.
- Generates interview questions based on the user's resume and job title.
- Accepts voice input as answers to interview questions.
- Evaluates similarity between user's answers and ideal answers using Gemini AI.
- Provides follow-up questions if similarity score is low.
- Stores similarity scores for analysis.
- Calculates and displays average similarity score at the end of the interview session.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ShreyasP20/AIvyinterviewer.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up Gemini API key.

4. Run the application:

```bash
python manage.py runserver
```

## Usage

1. Launch the application.
2. Provide your job title.
3. Upload your resume (PDF or image).
4. Follow the prompts to answer interview questions.
5. Receive feedback on your answers and improve your interview skills.

## Code Snippets

```python
# Calculate similarity score
tokens1 = set(word_tokenize(current_answer.lower())) - set(stopwords.words('english'))
tokens2 = set(word_tokenize(ideal_nu_answer.lower())) - set(stopwords.words('english'))
similarity_score = len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))


## Showcase

The project showcases multi-model integration and demonstrates how Gemini tools have been utilized for interview preparation, emphasizing their effectiveness in tackling interview challenges in the competitive job market.

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
