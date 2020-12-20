from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
import re
from textblob import TextBlob
from nltk.corpus import stopwords
# from text_summarizer import summarizer
from gensim.summarization.summarizer import summarize
contractions = {
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"i'd": "i would",
"i'll": "i will",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"must've": "must have",
"mustn't": "must not",
"needn't": "need not",
"oughtn't": "ought not",
"shan't": "shall not",
"sha'n't": "shall not",
"she'd": "she would",
"she'll": "she will",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"that'd": "that would",
"that's": "that is",
"there'd": "there had",
"there's": "there is",
"they'd": "they would",
"they'll": "they will",
"they're": "they are",
"they've": "they have",
"wasn't": "was not",
"we'd": "we would",
"we'll": "we will",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"where'd": "where did",
"where's": "where is",
"who'll": "who will",
"who's": "who is",
"won't": "will not",
"wouldn't": "would not",
"you'd": "you would",
"you'll": "you will",
"you're": "you are"
}
class ReviewAnalysis:
    def __init__(self,):
        self.reviews=[]
        self.keywords=[]
        self.n_reviews=[]
        self.p_reviews=[]
        self.sentiment=None
    #flair_sentiment = flair.models.TextClassifier.load('en-sentiment')
    def predictSentiment(self, sentence):
        #s = flair.data.Sentence(sentence)
        #flair_sentiment.predict(s)
        #total_sentiment = s.labels
        #print(total_sentiment)
        return TextBlob(sentence).sentiment.polarity
    #sentence="it's not very good"
    #predictSentiment(sentence)
    def getReviews(self,reviews):
        self.reviews=reviews
    def clean_text(self, text, remove_stopwords=True):
        # Convert words to lower case
        text = text.lower()
        # Replace contractions with their longer forms
        if True:
            text = text.split()
            new_text = []
            for word in text:
                if word in contractions:
                    new_text.append(contractions[word])
                else:
                    new_text.append(word)
            text = " ".join(new_text)
        # Format words and remove unwanted characters
        text = re.sub(r'https?:\/\/.*[\r\n]*', '', text,
                      flags=re.MULTILINE)
        text = re.sub(r'\<a href', ' ', text)
        text = re.sub(r'&amp;', '', text)
        text = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/]', ' ', text)
        text = re.sub(r'<br />', ' ', text)
        text = re.sub(r'\'', ' ', text)
        # Optionally, remove stop words
        if remove_stopwords:
            text = text.split()
            stops = set(stopwords.words("english"))
            text = [w for w in text if not w in stops]
            text = " ".join(text)
        return text
    def OutputSentimentScore(self):
        n,p=0,0
        for review in self.reviews:
            cleanedReview=self.clean_text(review, remove_stopwords=True)
            s=self.predictSentiment(cleanedReview)
            if s<0:
                n+=1
                self.n_reviews.append(review)
            else:
                p+=1
                self.p_reviews.append(review)
        self.sentiment=float(p)*100.00/float((n+p))
        return self.sentiment
    def outputReviews(self):
        output_reviews=[]
        if self.sentiment<50:
            output_reviews+=self.n_reviews[0:10]
        else:
            output_reviews += self.p_reviews[0:10]

    def outputSummaries(self, input_text):
    
        model = T5ForConditionalGeneration.from_pretrained('t5-small')
        tokenizer = T5Tokenizer.from_pretrained('t5-small')
        device = torch.device('cpu')
        preprocess_text = input_text.strip().replace('\n','')
        t5_prepared_Text = "summarize: " + preprocess_text
        # print ('original text preprocessed: \n', preprocess_text)
        tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors='pt').to(device)
        # summmarize
        summary_ids = model.generate(tokenized_text,
                                            num_beams=4,
                                            no_repeat_ngram_size=2,
                                            min_length=30,
                                            max_length=100,
                                            early_stopping=True)
        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return output


    def calculateScore(self, VaccineSentiment, reviewsSentiment,cases, deaths, safetyGuideLines=True):
        score=0
        if VaccineSentiment=="Positive" or VaccineSentiment=="POSITIVE":
            score+=1
        if reviewsSentiment=="Positive" or reviewsSentiment=="POSITIVE":
            score+=1
        if safetyGuideLines:
            score+=1
        if cases<100:
            score+=1
        if deaths<1:
            score+=1
        return score


if __name__ == "__main__":
    ra = ReviewAnalysis()
    review = "On October 26th, my wife and two kids went to get hair cuts and colors.  The stylist (also the manager) was very polite and nice.  My daughter has wanted to get purple tips for a long time, so we indulged her.  My wife got her haircut and dyed and my other daughter just got a hair cut.  Everything looked great and everyone loved their hair.  It was a little expensive ($353.00) with the haircuts, tips bleached and dyed, a color, shampoo and conditioner for dyed hair, and a tip, but we loved the way everyone looked.Four days go by and my daughters tips were starting to lighten.  We didn't think much of it, because the color will mellow out after a few days.  By day nine, her tips had faded to a light blue.  We called the shop that evening to ask if they could do anything about her tips.  We were told that they didn't use a permanent or semi permanent dye, but a fashion dye which only lasts a couple of weeks. When we went to the shop, we asked for a permanent dye, due to the costs being so high.  We were told that what they were using was a permanent dye.  I told the stylist on the phone this and she said supercuts only has a 7 day color guarantee, but we could come in and they would dye her hair again for the same cost.  I asked to speak to the manager and was told she wasn't in the store at the time, but they would call me bac Updated 11/30/20. After talking to the manager and the owner, they made this right and fixed my daughter's hair.  We're very pleased with the results, and I'd like to thank Victoria (the manager) and the owner for their quick and courteous service.  While I was there I also got a quick buzz from one of the other stylist and she did a great job."
    review2 = "We were just looking for a place to sneak away and meet our adult children and their spouses; to get away from work and Covid-closures. The location was perfect as we were able to maintain our “social distance” together, enjoy the river, and relax!"
    ra.outputSummaries(review)
    print(ra.predictSentiment(review))