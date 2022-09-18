import unittest
from requests.exceptions import Timeout

from semanticscholar.SemanticScholar import SemanticScholar


class SemanticScholarTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sch = SemanticScholar()

    def test_paper(self):
        data = self.sch.get_paper('10.1093/mind/lix.236.433')
        self.assertEqual(data.title,
                         'Computing Machinery and Intelligence')
        self.assertEqual(data.raw_data['title'],
                         'Computing Machinery and Intelligence')
        self.sch.timeout = 0.01
        self.assertRaises(Timeout,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433')

    def test_author(self):
        data = self.sch.get_author(2262347)
        self.assertEqual(data.name, 'A. Turing')
        self.assertEqual(data.raw_data['name'], 'A. Turing')

    def test_not_found(self):
        data = self.sch.get_paper(0).raw_data
        self.assertEqual(len(data), 0)

    def test_search(self):
        data = self.sch.search_paper('turing')
        self.assertGreater(data.total, 0)
        self.assertGreater(data.next, 0)
        data.next_page()
        self.assertGreater(len(data), 100)


if __name__ == '__main__':
    unittest.main()
