import semanticscholar as sch
from unittest import TestCase

def test_paper():
    data = sch.paper('10.1038/nrn3241')
    assert data['title'] == 'The origin of extracellular fields and currents — EEG, ECoG, LFP and spikes'
    
def test_author():
    data = sch.author(1741101)
    assert data['name'] == 'Oren Etzioni'