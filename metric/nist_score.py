import math
from .tool.n_gram import ngrams
from .tool.counter_element import counter_element
from .tool.overlaps_dict import overlaps_dict


class nist:
  """

    model = nist_score()
    model.fit(["this is a blue ball and a good ball", "this color of ball id blue and good"], "the the the bal is bluu and god")
      --->0.896865710312585

  """
  def __init__(self, n = 5):
    """ 
      Quantification for number n-grams 
    """ 
    self.number_n_grams = n
  
  def nist_score(self, refs, pred): 

    """
      refs ---> [ref1, ref2, ref3, ...] and pred is str
      Calculation of n-grams for different amounts
    """
    pred_ngrams = [ngrams(pred, n) for n in range(1 , self.number_n_grams + 1)]
    refs_ngrams = [[ngrams(ref, n) for n in range(1, self.number_n_grams + 1)] for ref in refs]

    """

      In all the obtained grammars, we can see that each element is repeated several times ---- > refs_ngrams_freq
      and

    """
    refs_ngrams_freq ,refs_total_words = dict() , 0
    for index in range(0, len(refs)):
      refs_total_words += len(refs[index].split())
      for num_gram in range(0, self.number_n_grams):
        count_ngrams = counter_element(refs_ngrams[index][num_gram])
        for element in count_ngrams:
          refs_ngrams_freq[element] = (refs_ngrams_freq[element] + count_ngrams[element]) if element in refs_ngrams_freq else 1

    info = self._info(refs_ngrams_freq, refs_total_words)

    """

      For each gram in X and each reference sentence in the references, 
      it first calculates no points and selects the highest one, 
      and then selects the reference sentences that caused the highest points to calculate the penalty.

    """

    nist_score , pred_lenght, ref_lenght = [], len(pred.split()), 0
    for n in range(0, self.number_n_grams):
      
      nist_precisions = list()
      for index_ref in range(0, len(refs)):
        ref_count_gram = counter_element(refs_ngrams[index_ref][n])
        pred_coumt_gram = counter_element(pred_ngrams[n])
        overlaps_ngram = overlaps_dict(ref_count_gram, pred_coumt_gram)
        numerator = sum([info[n_gram] * count for n_gram, count in overlaps_ngram.items()])
        denominator = sum(pred_coumt_gram.values())
        nist_precisions.append(numerator / denominator)
      nist_score.append(max(nist_precisions))
      ref_lenght += len(refs[nist_precisions.index(max(nist_precisions))].split())
    
    return sum(nist_score) * self._length_penalty(ref_lenght / self.number_n_grams, pred_lenght)
    



  def _info(self, refs_ngrams_freq, refs_total_words):
    """

      Here we calculate the weight for members of refs_ngrams_freq
      According to the formula -----‌> log2(occurrence w1, w2, ... wn-1, occurrence w1, w2, ... wn)

    """
    info = dict()
    for grams_1n in refs_ngrams_freq:
      grams_1m = grams_1n[ : -1] #w1, w2, ... wn-1
      occurrence = refs_ngrams_freq[grams_1m] if grams_1m and grams_1m in refs_ngrams_freq else refs_total_words
      info[grams_1n] = math.log(occurrence / refs_ngrams_freq[grams_1n], 2)
    return info



  def _length_penalty(self, refs_lenght, pred_lenght):


    """
      The penalty rate to be calculated
      Here, β is chosen so that the brevity penalty factor = 0.5 when the number of words
      in the hypothesis is 2/3 of the average number of words in the reference. |r̄ | means the
      average number of words in the reference.
    """


    ratio = pred_lenght / refs_lenght
    if 0 < ratio < 1:
        beta = math.log(0.5) / math.log(1.5) ** 2
        return math.exp(beta * math.log(ratio) ** 2)
    else:  
        return 1


