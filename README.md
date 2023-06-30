# Enhancement_of_Text_Data_Using_NLP_And_Machine_Learning_Models

This project focuses on improving the quality and quantity of text data through the integration of Natural Language Processing (NLP) techniques and machine learning models. The primary objective is to enhance the text data for better analysis and modeling. Here is an overview of the project's key steps:

**Converting to DataFrame**: Convert raw text data into a structured DataFrame format, enabling easier manipulation and analysis.

**Pre-Processing**: Apply various pre-processing techniques to clean and normalize the text data. These steps include converting the text to lowercase, removing emoticons and punctuation marks, splitting the text into a list by eliminating whitespaces, and performing lemmatization to reduce words to their base forms.

**Amplification of Data**: Enhance the existing data by generating additional samples using data augmentation techniques. The project employs the following methods:

1. Embedding Augmenter: Utilize word embeddings to create similar yet distinct sentessnces by replacing specific words with synonyms or related words based on word embeddings.

2. WordNet Augmenter: Utilize WordNet, a lexical database, to replace words in the original sentences with their synonyms, thus generating new variations.

3. EasyData Augmenter: Introduce noise into the data through transformations like shuffling, random deletion, and random word swapping. This diversifies the dataset and improves model robustness.

4. CheckList: Generate new sentences by applying predefined lexical transformations such as negation, intensification, and antonym replacement. This creates instances with altered sentiment or meaning.

**Preparing Data for Model**: Prepare the augmented dataset for model training. This involves splitting the data into training and validation sets and converting the text data into numerical representations suitable for machine learning models. Common approaches include Term Frequency-Inverse Document Frequency (TF-IDF) vectorization.

**Classification with Minimal Use of ML Techniques**: Train a baseline model using minimal machine learning techniques. This may include simple algorithms or rule-based approaches to classify the text data into different categories based on sentiment or other predefined labels.

**Logistic Regression**: Train a Logistic Regression model using the pre-processed and augmented data to predict sentiment or other target labels associated with the text.

**Analysis of the Model**: Gain insights into the model's performance and understand its predictions using the eli5 library. This library provides tools for explaining machine learning models by displaying feature weights and contributions. The eli5.show_prediction() function can be used to visualize the top 10 important features and their contributions for a specific example.

Overall, the project aims to enhance text data through NLP techniques, including data augmentation, and leverage machine learning models such as Logistic Regression for text classification and prediction tasks. The eli5 library is employed for model analysis and interpretation, providing insights into the model's performance and key features contributing to predictions.
