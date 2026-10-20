"""Contract tests for Hoàng data/extraction; do not require full benchmark."""
import io
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from data.shared import ContractError,load_and_validate,eligible,theorem_id,SOURCE_COMMIT,POOL_ID


def records(*data):
    return io.BytesIO((''.join(json.dumps(d,ensure_ascii=False)+'\n' for d in data)).encode('utf-8'))


def corpus(name):
    return {'id':name,'name':name,'statement':'theorem true','namespace':'Mathlib','source_commit':SOURCE_COMMIT}


def query(rels):
    return {'id':'QMathlib.example','statement':'theorem true','relevant_ids':rels,'split':'test','pool_id':POOL_ID}

class SharedContractTest(unittest.TestCase):
    def test_valid(self):
        result=load_and_validate(records(corpus('Mathlib.example'),corpus('Mathlib.helper')),
               records(query(['Mathlib.helper'])),strict_counts=False)
        self.assertEqual(result['direct_premise_labels'],1)
    def test_self_not_eligible(self):
        self.assertEqual(theorem_id('QMathlib.example'),'Mathlib.example')
        self.assertFalse(eligible('Mathlib.example','QMathlib.example'))
        self.assertTrue(eligible('Mathlib.helper','QMathlib.example'))
    def test_self_ground_truth_rejected(self):
        with self.assertRaises(ContractError):
            load_and_validate(records(corpus('Mathlib.example')),records(query(['Mathlib.example'])),strict_counts=False)
    def test_missing_ground_truth_rejected(self):
        with self.assertRaises(ContractError):
            load_and_validate(records(corpus('Mathlib.example')),records(query(['Nonexistent'])),strict_counts=False)
    def test_bad_commit_rejected(self):
        bad=corpus('Mathlib.example');bad['source_commit']='different'
        with self.assertRaises(ContractError):
            load_and_validate(records(bad),records(query(['Mathlib.helper'])),strict_counts=False)
    def test_other_test_theorem_allowed(self):
        self.assertTrue(eligible('Mathlib.other_test_theorem','QMathlib.example'))
    def test_duplicate_document_rejected(self):
        with self.assertRaises(ContractError):
            load_and_validate(records(corpus('Mathlib.example'),corpus('Mathlib.example')),records(query(['Mathlib.example'])),strict_counts=False)

if __name__=='__main__':unittest.main()
