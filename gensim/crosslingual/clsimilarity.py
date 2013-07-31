import languages
import gsimilarity

class Similarity():
    def __init__(self, lang1, lang2, mm_path, model_path):
        # mm_path is output folder of make_wikicorpus.py
        # model_path is output folder of build_lsi.py
        self.model = gsimilarity.GSimilarity(lang1, lang2, mm_path, model_path)
        
    def compare(self, text1, text2):
        similarity = self.model.compare(text1, text2)
        return similarity

class SimilarityMulti():
    """
    This class is to be used if you have trained more than one model ("sl_en", "sl_de", ...) and want to enable
    automatic detection of language of texts which are to be compared.
    """
    def __init__(self, model_paths):
        # mm_path is output folder of make_wikicorpus.py
        # model_path is output folder of build_lsi.py
        self.model_paths = model_paths # {"sl_en":(mm_path, model_path), "sl_de": ...} 
        self.models = {}
        for model, (mm_path, model_path) in self.model_paths.iteritems():
            lang1 = model.split("_")[0]
            lang2 = model.split("_")[1]
            self.models[model] = gsimilarity.GSimilarity(lang1, lang2, mm_path, model_path)
        self.langs = languages.Languages()
        
    def compare(self, text1, text2, lang1=None, lang2=None):
        if lang1 == None:
            lang1 = self.langs.detect_lang(text1)
        if lang2 == None:
            lang2 = self.langs.detect_lang(text2)
        model = self.models["%s_%s" % (lang1, lang2)]
        similarity = model.compare(text1, text2)
        return similarity
    
    
if __name__ == "__main__":
    # for testing
    mm_path = "/home/miha/Desktop/starcluster-downloaded/sl_en"
    model_path = "/home/miha/Desktop/wiki-models/sl_en"
    #mm_path = "/home/miha/wikipedia/sl_en"
    #model_path = "/home/miha/workspace/gensim/gensim/scripts/models/sl_en"
    model_paths = {"sl_en" : (mm_path, model_path)}
    #cl = SimilarityMulti(model_paths)
    cl = Similarity("sl", "en", mm_path, model_path)
    print cl.compare("drevo je rastlina, ni pa jabolko", "tree is a fruit")
    print cl.compare("drevo je rastlina, ni pa jabolko", "your shoes are blue")
    