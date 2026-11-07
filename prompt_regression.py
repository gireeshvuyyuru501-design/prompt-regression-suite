"""Reproducible offline prompt-configuration regression baseline.
No LLM is invoked: configurations select different extractive heuristics.
"""
import argparse
import json
import re
import urllib.request
from pathlib import Path

URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json"

def normalize(s):
    s = re.sub(r"[^\w\s]", " ", s.lower())
    return " ".join(w for w in s.split() if w not in {"a", "an", "the"})

def f1(pred, truth):
    from collections import Counter
    a, b = normalize(pred).split(), normalize(truth).split()
    if not a or not b:
        return float(a == b)
    overlap = sum((Counter(a) & Counter(b)).values())
    return 2 * overlap / (len(a) + len(b)) if overlap else 0.0

def exact_match(pred, truth):
    return float(normalize(pred) == normalize(truth))

def extract(context, question, version):
    """Two transparent offline answer-extraction heuristics, NOT prompt executions."""
    sentences = re.split(r"(?<=[.!?])\s+", context)
    if version == 'baseline':
        return sentences[0].strip() if sentences else ''
    qwords = set(normalize(question).split()) - {'what','who','when','where','which','why','how','is','was','did','does','of','in','to'}
    return max(sentences, key=lambda s: len(set(normalize(s).split()) & qwords), default='').strip()

def load_examples(path, limit):
    if not path.exists():
        print(f"Downloading public SQuAD dataset from {URL}")
        urllib.request.urlretrieve(URL, path)
    raw = json.loads(path.read_text(encoding='utf-8'))
    out = []
    for article in raw['data']:
        for paragraph in article['paragraphs']:
            for qa in paragraph['qas']:
                if qa.get('answers'):
                    out.append({'id': qa['id'], 'context': paragraph['context'], 'question': qa['question'], 'answers': [a['text'] for a in qa['answers']]})
                    if len(out) >= limit:
                        return out
    return out

def evaluate(examples, version):
    rows=[]
    for ex in examples:
        prediction=extract(ex['context'],ex['question'],version)
        rows.append({'id':ex['id'],'prediction':prediction,'em':max(exact_match(prediction,a) for a in ex['answers']), 'f1':max(f1(prediction,a) for a in ex['answers'])})
    n=len(rows)
    return {'version':version,'exact_match':sum(r['em'] for r in rows)/n if n else 0,'f1':sum(r['f1'] for r in rows)/n if n else 0,'rows':rows}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--limit',type=int,default=100)
    parser.add_argument('--dataset',default='squad_validation.json')
    parser.add_argument('--output',default='regression_report.json')
    args=parser.parse_args()
    examples=load_examples(Path(args.dataset),args.limit)
    baseline=evaluate(examples,'baseline'); candidate=evaluate(examples,'candidate')
    report={'dataset':'SQuAD v1.1 validation','source':URL,'sample_count':len(examples),'live_llm_evaluated':False,'note':'Offline extractive heuristic comparison; NOT measured prompt or Gemini performance.','baseline':{'exact_match':baseline['exact_match'],'f1':baseline['f1']},'candidate':{'exact_match':candidate['exact_match'],'f1':candidate['f1']},'delta':{'exact_match':candidate['exact_match']-baseline['exact_match'],'f1':candidate['f1']-baseline['f1']},'examples': [{'id':a['id'],'baseline_em':a['em'],'candidate_em':b['em'],'baseline_f1':a['f1'],'candidate_f1':b['f1']} for a,b in zip(baseline['rows'],candidate['rows'])]}
    Path(args.output).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='examples'},indent=2))
    print(f"Saved {args.output}")

if __name__=='__main__': main()
