import semanticscholar as sch
import unittest
from requests.exceptions import Timeout


class SemanticScholarTest(unittest.TestCase):
    def test_paper(self):
        data = sch.paper('10.1093/mind/lix.236.433', timeout=5)
        self.assertEqual(data['title'],
                         'Computing Machinery and Intelligence')

        self.assertRaises(Timeout,
                          sch.paper,
                          '10.1093/mind/lix.236.433',
                          timeout=0.01)

    def test_author(self):
        data = sch.author(2262347, timeout=5)
        self.assertEqual(data['name'], 'A. Turing')

    def test_not_found(self):
        data = sch.paper(0, timeout=5)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
