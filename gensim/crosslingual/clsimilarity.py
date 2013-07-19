import languages
import gsimilarity

class CLSimilarity():
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
        
    def compare(self, text1, text2):
        lang1 = self.langs.detect_lang(text1)
        lang2 = self.langs.detect_lang(text2)
        model = self.models["%s_%s" % (lang1, lang2)]
        similarity = model.compare(text1, text2)
        return similarity
    
    
if __name__ == "__main__":
    model_paths = {"sl_en" : ("/home/miha/Desktop/starcluster-downloaded/sl_en", 
                              "/home/miha/Desktop/wiki-models/sl_en")}
    cl = CLSimilarity(model_paths)
    print cl.compare("drevo je rastlina, ni pa jabolko", "tree is a fruit")
    print cl.compare("drevo je rastlina, ni pa jabolko", "do you see your shoes")
    