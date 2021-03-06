from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest
from collections import Counter

class FrequencySummarizer:
  def __init__(self, min_cut=0.1, max_cut=0.9):
    """
     Initilize the text summarizer.
     Words that have a frequency term lower than min_cut 
     or higer than max_cut will be ignored.
    """
    self._min_cut = min_cut
    self._max_cut = max_cut 
    self._stopwords = set(stopwords.words('english') + list(punctuation))

  def _compute_frequencies(self, word_sent):
    """ 
      Compute the frequency of each of word.
      Input: 
       word_sent, a list of sentences already tokenized.
      Output: 
       freq, a dictionary where freq[w] is the frequency of w.
    """
    freq = Counter()
    for s in word_sent:
      for word in s:
        if word not in self._stopwords:
          freq[word] += 1
    # frequencies normalization and fiteringz
    vals = freq.values()
    uniq = set(vals)
    if len(uniq) == 1:
      return freq
    new_freq = Counter()
    m = float(max(freq.values()))
    for w in freq.keys():
      val = freq[w]/m
      if val < self._max_cut and val > self._min_cut:
        new_freq[w] = val
    return new_freq

  def summarize(self, text, n):
    """
      Return a list of n sentences 
      which represent the summary of text.
    """
    sents = sent_tokenize(text)
    assert n <= len(sents)
    word_sent = [word_tokenize(s.lower()) for s in sents]
    self._freq = self._compute_frequencies(word_sent)
    ranking = Counter()
    for i,sent in enumerate(word_sent):
      for w in sent:
        if w in self._freq:
          ranking[i] += self._freq[w]
    sents_idx = self._rank(ranking, n)
    return [(sents[j], ranking[j]) for j in sents_idx]

  def _rank(self, ranking, n):
    """ return the first n sentences with highest ranking """
    return nlargest(n, ranking, key=ranking.get)


