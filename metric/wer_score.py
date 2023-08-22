import numpy as np
import string

class wer:
  def __init__(self):
    """
      ref = "the dog is under the table"
      pred = "The dog is the fable"
      score = model.fit(pred, ref)
        ----> 0.33
      model.get_detail()
        ----> {'delete': 0, 'insert': 1, 'substitution': 1, 'same words': 4}

    """
    pass


  def wer_score(self, ref, pred):
    """
      We used the distance matrix to calculate the number of titles below : 
        1 --- > delete
        2 --- > insert
        3 --- > substitution

        we use backtrcing method and dynamic programming 

    """
    pred = self._preproocess(pred)
    ref = self._preproocess(ref)

    """
      Define the numbers used 
        1 -- > same words
        2 ---> insert
        3 ---> delete
        4 ---> substitution
    """

    costs = np.zeros((1 + len(pred), 1 + len(ref)))
    backtrace = np.zeros((1 + len(pred), 1 + len(ref)))

    costs[0] = [j for j in range(0, len(ref) + 1)]
    backtrace[0][ : ] = 2


    costs[ : , 0] = [j for j in range(0, len(pred) + 1)]
    backtrace[ : ][0] = 3

    backtrace[0][0] = 10 #None


    for row in range(1 , len(pred) + 1):
      for  col in range(1, len(ref) + 1):
        if pred[row - 1] == ref[col - 1]:
          costs[row][col] = costs[row - 1][col - 1]
          backtrace[row][col] = 1
        else:
          substitution = costs[row - 1][col - 1]
          delete = costs[row - 1][col]
          insert = costs[row][col - 1]
          fainal_cost = min(delete, insert, substitution)
          costs[row][col] = fainal_cost + 1
          if fainal_cost == delete:
            backtrace[row][col] = 3
          elif fainal_cost == insert:
            backtrace[row][col] = 2
          elif fainal_cost == substitution:
            backtrace[row][col] = 4

    i, j = len(pred), len(ref)
    self.num_same , self.num_del, self.num_sub, self.num_ins = 0, 0, 0, 0

    while i > 0 or j > 0:
      if backtrace[i][j] == 1:
        i -= 1
        j -= 1
        self.num_same += 1

      if backtrace[i][j] == 4:
        i -= 1
        j -= 1
        self.num_sub += 1


      if backtrace[i][j] == 2:
        j -= 1
        self.num_ins += 1

      if backtrace[i][j] == 3:
        i -= 1
        self.num_del += 1


    return (self.num_del + self.num_sub + self.num_ins) / len(ref)

  def _preproocess(self, text):

    """

      It preprocesses the data to prepare it for processing, 
      which includes lowercase all letters, remove punctuation marks, and tokenize words.
      
    """
    persian_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
    punctuations_list = string.punctuation + persian_punctuations
    text = text.lower()
    translator = str.maketrans('', '', punctuations_list)
    text = text.translate(translator)
    text = text.split()
    return text


  def get_detail(self):
    return {
      "delete" : self.num_del,
      "insert" : self.num_ins,
      "substitution" : self.num_sub,
      "same words" : self.num_same
    }


