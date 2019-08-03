import semanticscholar as sch
from unittest import TestCase

def test_paper():
    data = sch.paper('10.1093/mind/LIX.236.433')
    assert data['title'] == 'Computing Machinery and Intelligence'
    
def test_author():
    data = sch.author(2262347)
    assert data['name'] == 'Alan M. Turing'