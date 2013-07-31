Cross-lingual gensim

This is a fork of Gensim where some cross-lingual capabilities are added to the WikiCorpus. Originally,
WikiCorpus iterates over articles inside Wikipedia XML dump. 
Here, you can find some additional functionality which at each iteration through XML dump
downloads counterpart Wikipedia article for some other language (the same article written in some other language).

This enables doing LSI over cross-lingual documents and comparing the similarity 
of the two texts written in different languages. 

The steps below are described for Slovenian-English cross-lingual case.

Required steps:

* Build WikiCorpus

  * download Wikipedia XML dump for the language which has a smaller amount of articles (Slovenian in this case: slwiki-latest-pages-articles.xml.bz2)
  
  * download slwiki-latest-langlinks.sql.gz (contains links from Slovenian articles to the counterpart articles in English) and unzip it
  
  * go into MySQL console and execute: create database sllanglinks
  
  * execute in the console: mysql -u root -p sllanglinks < slwiki-latest-langlinks.sql
  
  * set MySQL username/password in wikicorpus.py
  
  * set the paths inside scripts/make_wikicorpus.py (BZ2 file, output folder, languages,)
  
  * execute make_wikicorpus.py

* Build LsiModel (set the paths inside scripts/build_lsi.py and execute it)

* Compute the similarity between Slovenian and English text::

	from gensim.crosslingual import clsimilarity
	mm_path = "/home/miha/Desktop/starcluster-downloaded/sl_en"
    model_path = "/home/miha/Desktop/wiki-models/sl_en"
    model_paths = {"sl_en" : (mm_path, model_path)}
    #cl = SimilarityMulti(model_paths)
    cl = Similarity("sl", "en", mm_path, model_path)
    print cl.compare("drevo je rastlina, ni pa jabolko", "tree is a fruit")
    print cl.compare("drevo je rastlina, ni pa jabolko", "your shoes are blue")

==============================================
gensim -- Python Framework for Topic Modelling
==============================================


Gensim is a Python library for *topic modelling*, *document indexing* and *similarity retrieval* with large corpora.
Target audience is the *natural language processing* (NLP) and *information retrieval* (IR) community.


Features
---------

* All algorithms are **memory-independent** w.r.t. the corpus size (can process input larger than RAM),
* **Intuitive interfaces**

  * easy to plug in your own input corpus/datastream (trivial streaming API)
  * easy to extend with other Vector Space algorithms (trivial transformation API)

* Efficient implementations of popular algorithms, such as online **Latent Semantic Analysis**,
  **Latent Dirichlet Allocation** or **Random Projections**
* **Distributed computing**: can run *Latent Semantic Analysis* and *Latent Dirichlet Allocation* on a cluster of computers.
* Extensive `HTML documentation and tutorials <http://radimrehurek.com/gensim/>`_.


If this feature list left you scratching your head, you can first read more about the `Vector
Space Model <http://en.wikipedia.org/wiki/Vector_space_model>`_ and `unsupervised
document analysis <http://en.wikipedia.org/wiki/Latent_semantic_indexing>`_ on Wikipedia.

Installation
------------

This software depends on `NumPy and Scipy <http://www.scipy.org/Download>`_, two Python packages for scientific computing.
You must have them installed prior to installing `gensim`.

It is also recommended you install a fast BLAS library prior to installing NumPy. This is optional, but using an optimized BLAS such as `ATLAS <http://math-atlas.sourceforge.net/>`_ or `OpenBLAS <http://xianyi.github.io/OpenBLAS/>`_ is known to improve performance by as much as an order of magnitude.

The simple way to install `gensim` is::

    sudo easy_install gensim

Or, if you have instead downloaded and unzipped the `source tar.gz <http://pypi.python.org/pypi/gensim>`_ package,
you'll need to run::

    python setup.py test
    sudo python setup.py install


For alternative modes of installation (without root privileges, development
installation, optional install features), see the `documentation <http://radimrehurek.com/gensim/install.html>`_.

This version has been tested under Python 2.5, 2.6 and 2.7, and should run on any 2.5 <= Python < 3.0.

Documentation
-------------

Manual for the gensim package is available in `HTML <http://radimrehurek.com/gensim/>`_. It
contains a walk-through of all its features and a complete reference section.
It is also included in the source distribution package.

----------------

Gensim is open source software, and has been released under the
`GNU LGPL license <http://www.gnu.org/licenses/lgpl.html>`_.
Copyright (c) 2009-2013 Radim Rehurek
