import json
import os
import re
REGEX = re.compile(r"\s+")

class Languages():
    def __init__(self): 
        module_dir = os.path.dirname(__file__)
        en_path = os.path.join(module_dir, "stopwords/english_stopwords.txt")
        it_path = os.path.join(module_dir, "stopwords/italian_stopwords.txt")
        de_path = os.path.join(module_dir, "stopwords/german_stopwords.txt")
        sl_path = os.path.join(module_dir, "stopwords/slovenian_stopwords.txt")
        en_stop = open(en_path).read()
        it_stop = open(it_path).read()
        de_stop = open(de_path).read()
        sl_stop = open(sl_path).read()
        self.en_stopwords = json.loads(en_stop)
        self.it_stopwords = json.loads(it_stop)
        self.de_stopwords = json.loads(de_stop)
        self.sl_stopwords = json.loads(sl_stop)
        
    def tokenize(self, text):
        return [tok.strip().lower() for tok in REGEX.split(text)]
    
    def detect_lang(self, text):
        tokens = self.tokenize(text)
        tokens_set = set(tokens)
        en_set = set(self.en_stopwords)
        it_set = set(self.it_stopwords)
        de_set = set(self.de_stopwords)
        sl_set = set(self.sl_stopwords)
        inter_en = en_set.intersection(tokens_set)
        inter_it = it_set.intersection(tokens_set)
        inter_de = de_set.intersection(tokens_set)
        inter_sl = sl_set.intersection(tokens_set)
        print "inter_en: %s" % len(inter_en)
        print "inter_it: %s" % len(inter_it)
        print "inter_de: %s" % len(inter_de)
        print "inter_sl: %s" % len(inter_sl)
        d = {}
        d["en"] = len(inter_en)
        d["it"] = len(inter_it)
        d["de"] = len(inter_de)
        d["sl"] = len(inter_sl)
        l = sorted(d.iteritems(), key=lambda t:t[1], reverse=True)[0][0]
        return l
    
    
    
    
    
    