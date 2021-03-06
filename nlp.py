from nltk.chunk import ChunkParserI
from nltk.chunk.util import conlltags2tree
from nltk.corpus import gazetteers


class LocationChunker(ChunkParserI):
    def __init__(self):
        self.locations = set(gazetteers.words())
        self.lookahead = 0
        for loc in self.locations:
            nwords = loc.count(' ')
            if nwords > self.lookahead:
                self.lookahead = nwords
    def iob_locations(self, tagged_sent):
        i = 0
        l = len(tagged_sent)
        inside = False
        while i < l:
            word, tag = tagged_sent[i]
            j = i + 1
            k = j + self.lookahead
            nextwords, nexttags = [], []
            loc = False

            while j < k:
                if ' '.join([word] + nextwords) in self.locations:
                    if inside:
                        yield word, tag, 'I-LOCATION'
                    else:
                        yield word, tag, 'B-LOCATION'
                    for nword, ntag in zip(nextwords, nexttags):
                        yield nword, ntag, 'I-LOCATION'
                    loc, inside = True, True
                    i = j
                    break
                if j < l:
                    nextword, nexttag = tagged_sent[j]
                    nextwords.append(nextword)
                    nexttags.append(nexttag)
                    j += 1
                else:
                    break
            if not loc:
                inside = False
                i += 1
                yield word, tag, 'O'

    def parse(self, tagged_sent):
        iobs = self.iob_locations(tagged_sent)
        return conlltags2tree(iobs)

'''
example usage: from chunkers import LocationChunker
t = loc.parse([('San', 'NNP'), ('Francisco', 'NNP'), ('CA',
'NNP'), ('is', 'BE'), ('cold', 'JJ'), ('compared', 'VBD'), ('to',
'TO'), ('San', 'NNP'), ('Jose', 'NNP'), ('CA', 'NNP')])
>>> sub_leaves(t, 'LOCATION')
[[('San', 'NNP'), ('Francisco', 'NNP'), ('CA', 'NNP')], [('San',
'NNP'), ('Jose', 'NNP'), ('CA', 'NNP')]]
'''