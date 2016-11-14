from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = "/media/barno/Files/work/coref/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0.jar"
path_to_models_jar = "/media/barno/Files/work/coref/stanford-corenlp-full-2015-12-09/stanford-corenlp-3.6.0-models.jar"
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
result = dependency_parser.raw_parse('I shot an elephant in my sleep')
dep = result.next()
list(dep.triples())