"""
Author : Asish Panda
email : asishrocks95@gmail.com


A Naive Baysian apporach to classify news articles into categories.
"""

class classify:

    def __init__(self):

        """
        self.trivial : list, stores strings which should not be considered for categorisation

        self.category: dict, stores different categories as keys and times they appeared as 
                       value for key.

        self.words : dict of form {word : {count: value, category: value}}

        self.sents : float, stores the number of news articles added to corpus
        """

        self.trivial = ["the", 'an', 'a', '.', ',', 'i', 'even', 'may']
        self.category = {}
        self.words = {}
        self.sents = 0.0

    def train(self, text, category):
        """
        Train a data set associated with the given category.

        Increments each value that we will require while classifying a new text
        """

        text = text.lower()
        words = text.split(' ')

        try:
            self.category[category] += 1.0
        except:
            self.category[category] = 1.0

        for word in words:

            if word in self.trivial:
                continue

            try:
                self.words[word]['count'] += 1.0
                try:
                    self.words[word][category] += 1.0
                except:
                    self.words[word][category] = 1.0

            except:
                self.words[word] = {}
                #create category for each word
                for cat in self.category.keys():
                    self.words[word][cat] = 1.0
                self.words[word]['count'] = 1.0

        self.sents += 1.0


    def classify(self, text):
        """
        classifies a text into a category. taken from previously trained data.

        Baysian formula:
            P(text/category) = mul(P(wordi/categoryi),  P(wordi+1/categoryi+1), ...., P(wordj/categoryj))

        The probabilty of a category being associated with a word is calculated. This is done for all set of
        words in the given text with respect to our obtained values in training data. These probabilty is 
        multiplied for each category and the category simply falls to the category having the max probabilty.

        """
        text = text.lower()
        words = text.split(' ')
        pcats = []
        for pcat in self.category.keys():
            pcats.append([self.category[pcat] / self.sents, pcat])
            #pcats.append([1, pcat])

        for word in words:
            #multiplication of probabilty of each word in the baysian formula
            if not word in self.words:
                continue

            for pcat in pcats:
                try:
                    pcat[0] *= self.words[word][pcat[1]] / self.words[word]['count']
                except:
                    continue
        return max(pcats)[1]


    def train_from_corpus(self):
        """
        A saved corpus is used as training data set for the algorithm.
        """

        #its important to save the data as a string object to maintain consistency in the 
        #code

        f = open('corpus/data.txt', 'r')
        lines = f.read()

        #start flag to check for the category
        start = True
        for line in lines.split():
            if start:
                text = ' '
                category = line.replace('<', '').replace('>', '')
                start = False

            elif line == '</' + category + '>':
                start = True
                self.train(text, category)

            else:
                text += line + ' '

        f.close()        

    def _add_into_corpus(self, text, category):
        """
        This method addes text extracted from website, or mannually entered in 
        a format which can be easily parsed.

        FORMAT
        ======
        <category> a long string, denoting the text you want to add into the corpus,
        which is followed by an ending tag represented as </category>

        """

        f = open('corpus/data.txt', 'a')
        f.write(' ')
        f.write( '<' + str(category) + '>' + ' ')
        f.write(str(text))
        f.write('</' + str(category) + '>')
        f.close()

    def _get_text_website(self, site):
        """
        This method extracts data from timesofindia website, useful for adding categorised
        data into corpus easily. The downside is, that it only parses one website data.
        """
        
        import requests

        r = requests.get(site)
        text = ''

        string = r.text
        string = string.replace('>', ' ')
        text_list = string.split(' ')
        found = False
        count = 1
 
        #check if found "Normal" and keep adding words to text
        for word in text_list:

            try:
                word = str(word)
            except:
                #Unicode is not supported, might be a good idea to consider
                #unicode characters
                continue

            if found:
                word = word.replace('"', ' ').replace('.', ' ').replace(',', ' ').replace('?',' ').replace('(', '').replace(')', '').replace('<br','')

                if word == '<div':
                    count += 1  

                elif word == '<meta':
                    break

                elif word == '</div':
                    count -= 1
                    if count == 0:
                        break

                elif not(word.startswith("<") or word.startswith("href")) and count == 1:
                    text += word + ' '


            elif word == 'class="Normal"':
                found = True

        return text        

    def classify_from_website(self, site):
        """
        classfies data extracted from a given timesofindia website into category
        """

        text = self._get_text_website(site)
        return self.classify(text)

    def add_into_corpus_website(self, site, category):
        """
        Extracts and adds data into corpus from timesofinda website.
        """

        text = self._get_text_website(site)
        self. _add_into_corpus(text, category)

        
if __name__ == '__main__':
    """
    Usage example
    =============
    
    
    p = classify()
    p.train_from_corpus()
    p.classify("http://timesofindia.indiatimes.com/tech/tech-news/YouTube-better-than-Facebook-for-video-advertisements-Report/articleshow/49205996.cms")
    
    **It should be noted that, this algorithm accuracy increases with increase in quantity of training data set. It is
    **also necessary to train the algorithm with some data before using.
    """
