import gensim
import os, bz2
from gensim.similarities import Similarity
from gensim.models import LsiModel, LogEntropyModel

class GSimilarity():
    def __init__(self, lang1, lang2, mm_path, model_path):
        self.lang1 = lang1
        self.lang2 = lang2
        self.id2word = gensim.corpora.Dictionary.load_from_bz2(
                    bz2.BZ2File(os.path.join(mm_path, 'wiki_%s_%s_wordids.txt.bz2' % (lang1, lang2))))
        self.tokenize_func = gensim.corpora.wikicorpus.tokenize  # The tokenizer used to create the Wikipedia corpus
        self.model_path = model_path
        # Log Entropy weights frequencies of all document features in the corpus
        self.logent_transformation = LogEntropyModel.load(os.path.join(self.model_path, "logent.model"))
        self.lsi_transformation = LsiModel.load(os.path.join(self.model_path, "lsi.model"))
        
    def compare(self, text1, text2):
        documents = [text1]
        corpus = (self.id2word.doc2bow(self.tokenize_func(document)) for document in documents)
        index = Similarity(corpus=self.lsi_transformation[self.logent_transformation[corpus]], num_features=100, output_prefix="shard")
        sims_to_query = index[self.lsi_transformation[self.logent_transformation[self.id2word.doc2bow(self.tokenize_func(text2))]]]
        sim = sims_to_query.tolist()[0]
        return sim

    