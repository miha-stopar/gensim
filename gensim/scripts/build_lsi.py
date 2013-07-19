# -*- coding: utf-8 -*-
import logging, gensim, bz2, pprint
import os, shutil

from gensim.similarities import Similarity
from gensim.models import LsiModel, LogEntropyModel

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

lang1 = "sl"
lang2 = "en"

# load id->word mapping (the dictionary), one of the results of step 2 above
#id2word = gensim.corpora.Dictionary.load_from_text('/home/miha/gensimAPI/%s_%s/wiki_%s_%s_wordids.txt' % (lang1, lang2, lang1, lang2))
id2word = gensim.corpora.Dictionary.load_from_bz2(
                    bz2.BZ2File('/home/miha/Desktop/starcluster-downloaded/%s_%s/wiki_%s_%s_wordids.txt.bz2' % (lang1, lang2, lang1, lang2)))
dictionary = id2word

# load corpus iterator
mm = gensim.corpora.MmCorpus('/home/miha/Desktop/starcluster-downloaded/%s_%s/wiki_%s_%s_tfidf.mm' % (lang1, lang2, lang1, lang2))
# mm = gensim.corpora.MmCorpus(bz2.BZ2File('wiki_en_tfidf.mm.bz2')) # use this if you compressed the TFIDF output (recommended)

print mm
wiki_corpus = mm

load_existing = False

tokenize_func = gensim.corpora.wikicorpus.tokenize  # The tokenizer used to create the Wikipedia corpus

### Chained transformations
# builds corpus from iterating over documents of bow_corpus as transformed to log entropy representation. Will also take many hours with Wikipedia corpus.
#logent_corpus = gensim.corpora.MmCorpus(corpus=logent_transformation[wiki_corpus], id2word=dictionary)  

# creates LSI transformation model from log entropy corpus representation. Takes several hours with Wikipedia corpus.
#lsi_transformation = LsiModel(corpus=logent_corpus, id2word=dictionary, num_topics=400)  

# Performs same operation as above, but with implicit chaining
root_path = "models/%s_%s" % (lang1, lang2)
if load_existing:
    # Log Entropy weights frequencies of all document features in the corpus
    logent_transformation = LogEntropyModel.load(os.path.join(root_path, "logent.model"))
    lsi_transformation = LsiModel.load(os.path.join(root_path, "lsi.model"))
else:
    logent_transformation = LogEntropyModel(wiki_corpus, id2word=dictionary)  
    lsi_transformation = LsiModel(corpus=logent_transformation[wiki_corpus], id2word=dictionary, num_topics=100)  
    
    if os.path.exists(root_path):
        shutil.rmtree(root_path)
    os.makedirs(root_path)
    
    # Can persist transformation models, too.
    logent_transformation.save(os.path.join(root_path, "logent.model"))
    lsi_transformation.save(os.path.join(root_path, "lsi.model"))

# print the most contributing words (both positively and negatively) for each of the first ten topics
#lsi.print_topics(10)

### Similarities (the best part)

#documents = ["A bear walked in the dark forest.",
#             "Tall trees have many more leaves than short bushes.",
#             "A starship may someday travel across vast reaches of space to other stars.",
#             "Difference is the concept of how two or more entities are not the same."]
documents = ["Drevo je padlo na tla.", "Visoki nebotičniki imajo malo oken.", "Janez je nesramen."]

# A corpus can be anything, as long as iterating over it produces a representation of the corpus documents as vectors.
corpus = (dictionary.doc2bow(tokenize_func(document)) for document in documents)

index = Similarity(corpus=lsi_transformation[logent_transformation[corpus]], num_features=400, output_prefix="shard")

print "Index corpus:"
pprint.pprint(documents)

print "Similarities of index corpus documents to one another:"
#pprint.pprint([s for s in index])

#query = "In the face of ambiguity, refuse the temptation to guess."
def compare(query, index, lsi_transformation, logent_transformation, dictionary, tokenize_func):
    sims_to_query = index[lsi_transformation[logent_transformation[dictionary.doc2bow(tokenize_func(query))]]]
    print "Similarities of index corpus documents to '%s'" % query
    print sims_to_query

    best_score = max(sims_to_query)
    index = sims_to_query.tolist().index(best_score)
    most_similar_doc = documents[index]
    print "The document most similar to the query is '%s' with a score of %.2f." % (most_similar_doc, best_score)

query = "Houses are buildings."
compare(query, index, lsi_transformation, logent_transformation, dictionary, tokenize_func)
print "----------------------------------------------------------"

query = "Tree has leaves."
compare(query, index, lsi_transformation, logent_transformation, dictionary, tokenize_func)
print "----------------------------------------------------------"





