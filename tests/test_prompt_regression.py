import unittest
from prompt_regression import normalize, f1, exact_match, extract, evaluate

class RegressionTests(unittest.TestCase):
    def test_normalize(self): self.assertEqual(normalize('The, Cat!'),'cat')
    def test_exact_match(self): self.assertEqual(exact_match('A cat','cat'),1)
    def test_f1(self): self.assertAlmostEqual(f1('red blue','red'),2/3)
    def test_candidate_selects_relevant_sentence(self):
        self.assertEqual(extract('Paris is in France. Berlin is in Germany.','Where is Berlin?','candidate'),'Berlin is in Germany.')
    def test_report_values(self):
        cases=[{'id':'1','context':'Paris is in France. Berlin is in Germany.','question':'Where is Berlin?','answers':['Berlin is in Germany.']}]
        self.assertEqual(evaluate(cases,'candidate')['exact_match'],1)
    def test_empty(self): self.assertEqual(evaluate([],'baseline')['f1'],0)

if __name__=='__main__': unittest.main()
