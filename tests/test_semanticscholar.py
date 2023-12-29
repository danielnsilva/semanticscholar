import io
import json
import sys
import unittest
import asyncio
from datetime import datetime
from httpx import TimeoutException
import vcr

from semanticscholar.Author import Author
from semanticscholar.AsyncSemanticScholar import AsyncSemanticScholar
from semanticscholar.Citation import Citation
from semanticscholar.Journal import Journal
from semanticscholar.Paper import Paper
from semanticscholar.PublicationVenue import PublicationVenue
from semanticscholar.Reference import Reference
from semanticscholar.SemanticScholar import SemanticScholar
from semanticscholar.SemanticScholarException import (
    BadQueryParametersException, ObjectNotFoundException)
from semanticscholar.Tldr import Tldr

test_vcr = vcr.VCR(
    cassette_library_dir='tests/data',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    record_mode=['new_episodes'],
    match_on=['uri', 'method', 'body'],
    drop_unused_requests=True
)

class SemanticScholarTest(unittest.TestCase):

    def setUp(self) -> None:
        self.sch = SemanticScholar()

    def test_author(self) -> None:
        file = open('tests/data/Author.json', encoding='utf-8')
        data = json.loads(file.read())
        item = Author(data)
        self.assertEqual(item.affiliations, data['affiliations'])
        self.assertEqual(item.authorId, data['authorId'])
        self.assertEqual(item.citationCount, data['citationCount'])
        self.assertEqual(item.externalIds, data['externalIds'])
        self.assertEqual(item.hIndex, data['hIndex'])
        self.assertEqual(item.homepage, data['homepage'])
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.paperCount, data['paperCount'])
        self.assertEqual(str(item.papers), str(data['papers']))
        self.assertEqual(item.url, data['url'])
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['name'], data['name'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_citation(self):
        file = open('tests/data/Citation.json', encoding='utf-8')
        data = json.loads(file.read())
        item = Citation(data)
        self.assertEqual(item.contexts, data['contexts'])
        self.assertEqual(item.intents, data['intents'])
        self.assertEqual(item.contextsWithIntent, data['contextsWithIntent'])
        self.assertEqual(item.isInfluential, data['isInfluential'])
        self.assertEqual(str(item.paper), str(data['citingPaper']))
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['contexts'], data['contexts'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_journal(self) -> None:
        file = open('tests/data/Paper.json', encoding='utf-8')
        data = json.loads(file.read())['journal']
        item = Journal(data)
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.pages, data['pages'])
        self.assertEqual(item.volume, data['volume'])
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), data['name'])
        self.assertEqual(item['name'], data['name'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_paper(self) -> None:
        file = open('tests/data/Paper.json', encoding='utf-8')
        data = json.loads(file.read())
        item = Paper(data)
        self.assertEqual(item.abstract, data['abstract'])
        self.assertEqual(str(item.authors), str(data['authors']))
        self.assertEqual(item.citationCount, data['citationCount'])
        self.assertEqual(item.citationStyles, data['citationStyles'])
        self.assertEqual(str(item.citations), str(data['citations']))
        self.assertEqual(item.corpusId, data['corpusId'])
        self.assertEqual(item.embedding, data['embedding'])
        self.assertEqual(item.externalIds, data['externalIds'])
        self.assertEqual(item.fieldsOfStudy, data['fieldsOfStudy'])
        self.assertEqual(item.influentialCitationCount,
                         data['influentialCitationCount'])
        self.assertEqual(item.isOpenAccess, data['isOpenAccess'])
        self.assertEqual(str(item.journal), str(data['journal']['name']))
        self.assertEqual(item.openAccessPdf, data['openAccessPdf'])
        self.assertEqual(item.paperId, data['paperId'])
        self.assertEqual(item.publicationDate, datetime.strptime(
            data['publicationDate'], '%Y-%m-%d'))
        self.assertEqual(item.publicationTypes, data['publicationTypes'])
        self.assertEqual(item.publicationVenue, data['publicationVenue'])
        self.assertEqual(item.referenceCount, data['referenceCount'])
        self.assertEqual(str(item.references), str(data['references']))
        self.assertEqual(item.s2FieldsOfStudy, data['s2FieldsOfStudy'])
        self.assertEqual(item.title, data['title'])
        self.assertEqual(str(item.tldr), data['tldr']['text'])
        self.assertEqual(item.url, data['url'])
        self.assertEqual(item.venue, data['venue'])
        self.assertEqual(item.year, data['year'])
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['title'], data['title'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_pubication_venue(self):
        file = open('tests/data/Paper.json', encoding='utf-8')
        data = json.loads(file.read())['citations'][0]['publicationVenue']
        item = PublicationVenue(data)
        self.assertEqual(item.alternate_names, data['alternate_names'])
        self.assertEqual(item.alternate_urls, data['alternate_urls'])
        self.assertEqual(item.id, data['id'])
        self.assertEqual(item.issn, data['issn'])
        self.assertEqual(item.name, data['name'])
        self.assertEqual(item.type, data['type'])
        self.assertEqual(item.url, data['url'])
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['name'], data['name'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_reference(self):
        file = open('tests/data/Reference.json', encoding='utf-8')
        data = json.loads(file.read())
        item = Reference(data)
        self.assertEqual(item.contexts, data['contexts'])
        self.assertEqual(item.intents, data['intents'])
        self.assertEqual(item.contextsWithIntent, data['contextsWithIntent'])
        self.assertEqual(item.isInfluential, data['isInfluential'])
        self.assertEqual(str(item.paper), str(data['citedPaper']))
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['contexts'], data['contexts'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_tldr(self) -> None:
        file = open('tests/data/Paper.json', encoding='utf-8')
        data = json.loads(file.read())['tldr']
        item = Tldr(data)
        self.assertEqual(item.model, data['model'])
        self.assertEqual(item.text, data['text'])
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), data['text'])
        self.assertEqual(item['model'], data['model'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    @test_vcr.use_cassette
    def test_get_paper(self):
        data = self.sch.get_paper('10.1093/mind/lix.236.433')
        self.assertEqual(data.title,
                         'Computing Machinery and Intelligence')
        self.assertEqual(data.raw_data['title'],
                         'Computing Machinery and Intelligence')

    @test_vcr.use_cassette
    def test_get_papers(self):
        list_of_paper_ids = [
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        data = self.sch.get_papers(list_of_paper_ids)
        for item in data:
            with self.subTest(subtest=item.paperId):
                self.assertIn(
                    'E. Duflo', [author.name for author in item.authors])

    @test_vcr.use_cassette
    def test_get_paper_authors(self):
        data = self.sch.get_paper_authors('10.2139/ssrn.2250500')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 0)
        self.assertEqual(len([item for item in data]), 4)
        self.assertEqual(data[0].name, 'E. Duflo')

    @test_vcr.use_cassette
    def test_get_paper_citations(self):
        data = self.sch.get_paper_citations('CorpusID:14514057')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item.paper.title for item in data]), 1849)
        self.assertEqual(
            data[0].paper.title,
            'Conceptualising the empowerment of caregivers raising children '
            'with developmental disabilities in Ethiopia: a qualitative study')

    @test_vcr.use_cassette
    def test_get_paper_references(self):
        data = self.sch.get_paper_references('CorpusID:1033682')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item for item in data]), 156)
        self.assertEqual(
            data[0].paper.title,
            'Controlled Sparsity via Constrained Optimization or: How I '
            'Learned to Stop Tuning Penalties and Love Constraints')

    @test_vcr.use_cassette
    def test_timeout(self):
        self.sch.timeout = 0.01
        self.assertEqual(self.sch.timeout, 0.01)
        self.assertRaises(TimeoutException,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433')

    @test_vcr.use_cassette
    def test_get_author(self):
        data = self.sch.get_author(2262347)
        self.assertEqual(data.name, 'A. Turing')

    @test_vcr.use_cassette
    def test_get_authors(self):
        list_of_author_ids = ['3234559', '1726629', '1711844']
        data = self.sch.get_authors(list_of_author_ids)
        list_of_author_names = ['E. Dijkstra', 'D. Parnas', 'I. Sommerville']
        self.assertCountEqual(
            [item.name for item in data], list_of_author_names)

    @test_vcr.use_cassette
    def test_get_author_papers(self):
        data = self.sch.get_author_papers(1723755, limit=100)
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item for item in data]), 879)
        self.assertEqual(data[0].title, 'SARS-CoV-2 hijacks p38β/MAPK11 to '
                         'promote virus replication')

    @test_vcr.use_cassette
    def test_not_found(self):
        methods = [self.sch.get_paper, self.sch.get_author]
        for method in methods:
            with self.subTest(subtest=method.__name__):
                self.assertRaises(ObjectNotFoundException, method, 0)

    @test_vcr.use_cassette
    def test_bad_query_parameters(self):
        self.assertRaises(BadQueryParametersException,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433',
                          fields=['unknown'])

    @test_vcr.use_cassette
    def test_search_paper(self):
        data = self.sch.search_paper('turing')
        self.assertGreater(data.total, 0)
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len(data.items), 100)
        self.assertEqual(
            data.raw_data[0]['title'],
            'Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, '
            'A Large-Scale Generative Language Model'
        )

    @test_vcr.use_cassette
    def test_search_paper_next_page(self):
        data = self.sch.search_paper('turing')
        data.next_page()
        self.assertGreater(len(data), 100)

    @test_vcr.use_cassette
    def test_search_paper_traversing_results(self):
        data = self.sch.search_paper('sublinear near optimal edit distance')
        all_results = [item.title for item in data]
        self.assertRaises(BadQueryParametersException, data.next_page)
        self.assertEqual(len(all_results), len(data.items))

    @test_vcr.use_cassette
    def test_search_paper_fields_of_study(self):
        data = self.sch.search_paper('turing', fields_of_study=['Mathematics'])
        self.assertEqual(data[0].s2FieldsOfStudy[0]['category'], 'Mathematics')

    @test_vcr.use_cassette
    def test_search_paper_year(self):
        data = self.sch.search_paper('turing', year=1936)
        self.assertEqual(data[0].year, 1936)

    @test_vcr.use_cassette
    def test_search_paper_year_range(self):
        data = self.sch.search_paper('turing', year='1936-1937')
        self.assertTrue(all([1936 <= item.year <= 1937 for item in data]))

    @test_vcr.use_cassette
    def test_search_paper_publication_types(self):
        data = self.sch.search_paper(
            'turing', publication_types=['JournalArticle'])
        self.assertTrue('JournalArticle' in data[0].publicationTypes)
        data = self.sch.search_paper(
            'turing', publication_types=['Book', 'Conference'])
        self.assertTrue(
            'Book' in data[0].publicationTypes or
            'Conference' in data[0].publicationTypes)

    @test_vcr.use_cassette
    def test_search_paper_venue(self):
        data = self.sch.search_paper('turing', venue=['ArXiv'])
        self.assertEqual(data[0].venue, 'arXiv.org')

    @test_vcr.use_cassette
    def test_search_paper_open_access_pdf(self):
        data = self.sch.search_paper('turing', open_access_pdf=True)
        self.assertTrue(data[0].openAccessPdf)

    @test_vcr.use_cassette
    def test_search_paper_publication_date_or_year(self):
        date_ranges = [
            "2020-01-01",
            "2020-01",
            "2020",
            "2020-01-01:2021-01-01",
            "2020-01-01:",
            ":2020-01-01",
            "2020:2021",
            "2020:",
            ":2021",
        ]
        for date_range in date_ranges:
            with self.subTest(date_range=date_range):
                data = self.sch.search_paper(
                    'turing', publication_date_or_year=date_range)
                self.assertTrue(len(data) > 0)

    def test_search_paper_publication_date_or_year_invalid(self):
        date_ranges = [
            "2020-01-012021-01-01",
            "2020-01-01:2021-01-",
            "2020-01-01:2020-"
        ]
        for date_range in date_ranges:
            with self.subTest(date_range=date_range):
                self.assertRaises(
                    ValueError,
                    self.sch.search_paper,
                    'turing',
                    publication_date_or_year=date_range
                )

    @test_vcr.use_cassette
    def test_search_paper_min_citation_count(self):
        data = self.sch.search_paper('turing', min_citation_count=1000)
        self.assertTrue(all([item.citationCount >= 1000 for item in data]))

    @test_vcr.use_cassette
    def test_search_author(self):
        data = self.sch.search_author('turing')
        self.assertGreater(data.total, 0)
        self.assertEqual(data.next, 0)

    @test_vcr.use_cassette
    def test_get_recommended_papers(self):
        data = self.sch.get_recommended_papers('10.2139/ssrn.2250500')
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_pool_from(self):
        data = self.sch.get_recommended_papers(
            '10.1145/3544585.3544600', pool_from="all-cs")
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_pool_from_invalid(self):
        self.assertRaises(ValueError,
                          self.sch.get_recommended_papers,
                          '10.1145/3544585.3544600', pool_from="invalid")

    @test_vcr.use_cassette
    def test_get_recommended_papers_from_lists(self):
        data = self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600'], ['10.1145/301250.301271'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_from_lists_positive_only(self):
        data = self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600', '10.1145/301250.301271'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_from_lists_negative_only(self):
        self.assertRaises(BadQueryParametersException,
                          self.sch.get_recommended_papers_from_lists,
                          [],
                          ['10.1145/3544585.3544600'])

    @test_vcr.use_cassette
    def test_limit_value_exceeded(self):
        test_cases = [
            (self.sch.get_paper_authors, '10.1093/mind/lix.236.433', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.get_paper_citations, '10.1093/mind/lix.236.433', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.get_paper_references, '10.1093/mind/lix.236.433', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.get_author_papers, 1723755, 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.search_author, 'turing', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.search_paper, 'turing', 101,
             'The limit parameter must be between 1 and 100 inclusive.'),
            (self.sch.get_recommended_papers, '10.1145/3544585.3544600', 501,
             'The limit parameter must be between 1 and 500 inclusive.'),
            (self.sch.get_recommended_papers_from_lists,
             ['10.1145/3544585.3544600'], 501,
             'The limit parameter must be between 1 and 500 inclusive.'),
        ]
        for method, query, upper_limit, error_message in test_cases:
            with self.subTest(method=method.__name__, limit=upper_limit):
                with self.assertRaises(ValueError) as context:
                    method(query, limit=upper_limit)
                    self.assertEqual(str(context.exception), error_message)
            with self.subTest(method=method.__name__, limit=0):
                with self.assertRaises(ValueError) as context:
                    method(query, limit=0)
                    self.assertEqual(str(context.exception), error_message)

    # These last two tests have some async and some sync parts, so 
    # the async parts are run manually using asyncio.run_until_complete()
    @test_vcr.use_cassette
    async def test_get_author_papers_async(self):
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.sch.get_author_papers(1723755, limit=100))
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item for item in data]), 940)
        self.assertEqual(data[0].title, 'SARS-CoV-2 hijacks p38\u03b2/MAPK11 to promote virus replication')

    @test_vcr.use_cassette
    async def test_get_paper_citations_async(self):
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(self.sch.get_paper_citations('CorpusID:49313245'))
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 1000)
        self.assertEqual(len([item.paper.title for item in data]), 6220)
        self.assertEqual(
            data[0].paper.title, 'Self-Attention Mechanism for Dynamic Multi-Step Rop '
                'Prediction Under Continuous Learning Structure')

    @test_vcr.use_cassette
    def test_empty_paginated_results(self):
        data = self.sch.search_paper('n0 r3sult s3arch t3rm')
        self.assertEqual(data.total, 0)

    @test_vcr.use_cassette
    def test_debug(self):
        with open('tests/data/debug_output.txt', 'r') as file:
            expected_output = file.read()
        captured_stdout = io.StringIO()
        sys.stdout = captured_stdout
        self.sch = SemanticScholar(debug=True, api_key='F@k3K3y')
        self.assertEqual(self.sch.debug, True)
        list_of_paper_ids = [
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        with self.assertRaises(PermissionError):
            self.sch.get_papers(list_of_paper_ids)
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_stdout.getvalue().strip(),
                         expected_output.strip())

class AsyncSemanticScholarTest(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.sch = AsyncSemanticScholar()

    @test_vcr.use_cassette
    async def test_get_paper_async(self):
        data = await self.sch.get_paper('10.1093/mind/lix.236.433')
        self.assertEqual(data.title,
                         'Computing Machinery and Intelligence')
        self.assertEqual(data.raw_data['title'],
                         'Computing Machinery and Intelligence')

    @test_vcr.use_cassette
    async def test_get_papers_async(self):
        list_of_paper_ids = [
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        data = await self.sch.get_papers(list_of_paper_ids)
        for item in data:
            with self.subTest(subtest=item.paperId):
                self.assertIn(
                    'E. Duflo', [author.name for author in item.authors])
    
    @test_vcr.use_cassette
    async def test_get_paper_authors_async(self):
        data = await self.sch.get_paper_authors('10.2139/ssrn.2250500')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 0)
        self.assertEqual(len([item for item in data]), 4)
        self.assertEqual(data[0].name, 'E. Duflo')

    @test_vcr.use_cassette
    async def test_get_paper_references_async(self):
        data = await self.sch.get_paper_references('CorpusID:49313245')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 0)
        self.assertEqual(len(data), 73)
        self.assertEqual(
            data[0].paper.title, 'Constituency Parsing with a Self-Attentive Encoder')
    
    @test_vcr.use_cassette
    async def test_timeout_async(self):
        self.sch.timeout = 0.01
        self.assertEqual(self.sch.timeout, 0.01)
        with self.assertRaises(TimeoutException):
            await self.sch.get_paper('10.1093/mind/lix.236.433')
    
    @test_vcr.use_cassette
    async def test_get_author_async(self):
        data = await self.sch.get_author(2262347)
        self.assertEqual(data.name, 'A. Turing')

    @test_vcr.use_cassette
    async def test_get_authors_async(self):
        list_of_author_ids = ['3234559', '1726629', '1711844']
        data = await self.sch.get_authors(list_of_author_ids)
        list_of_author_names = ['E. Dijkstra', 'D. Parnas', 'I. Sommerville']
        self.assertCountEqual(
            [item.name for item in data], list_of_author_names)

    @test_vcr.use_cassette
    async def test_not_found_async(self):
        with self.assertRaises(ObjectNotFoundException):
            await self.sch.get_paper(0)
        with self.assertRaises(ObjectNotFoundException):
            await self.sch.get_author(0)

    @test_vcr.use_cassette
    async def test_bad_query_parameters_async(self):
        with self.assertRaises(BadQueryParametersException):
            await self.sch.get_paper('10.1093/mind/lix.236.433', fields=['unknown'])

    @test_vcr.use_cassette
    async def test_search_paper_async(self):
        data = await self.sch.search_paper('turing')
        self.assertGreater(data.total, 0)
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len(data.items), 100)
        self.assertEqual(
            data.raw_data[0]['title'],
            'Using DeepSpeed and Megatron to Train Megatron-Turing NLG 530B, '
            'A Large-Scale Generative Language Model')

    @test_vcr.use_cassette
    async def test_search_paper_next_page_async(self):
        data = await self.sch.search_paper('turing')
        await data.async_next_page()
        self.assertGreater(len(data), 100)

    @test_vcr.use_cassette
    async def test_search_paper_traversing_results_async(self):
        data = await self.sch.search_paper('sublinear near optimal edit distance')
        all_results = [item.title for item in data]
        with self.assertRaises(BadQueryParametersException):
            await data.next_page()
        self.assertEqual(len(all_results), len(data.items))

    @test_vcr.use_cassette
    async def test_search_paper_fields_of_study_async(self):
        data = await self.sch.search_paper('turing', fields_of_study=['Mathematics'])
        self.assertEqual(data[0].s2FieldsOfStudy[0]['category'], 'Mathematics')

    @test_vcr.use_cassette
    async def test_search_paper_year_async(self):
        data = await self.sch.search_paper('turing', year=1936)
        self.assertEqual(data[0].year, 1936)

    @test_vcr.use_cassette
    async def test_search_paper_year_range_async(self):
        data = await self.sch.search_paper('turing', year='1936-1937')
        self.assertTrue(all([1936 <= item.year <= 1937 for item in data]))

    @test_vcr.use_cassette
    async def test_search_paper_publication_types_async(self):
        data = await self.sch.search_paper(
            'turing', publication_types=['JournalArticle'])
        self.assertTrue('JournalArticle' in data[0].publicationTypes)
        data = await self.sch.search_paper(
            'turing', publication_types=['Book', 'Conference'])
        self.assertTrue(
            'Book' in data[0].publicationTypes or
            'Conference' in data[0].publicationTypes)

    @test_vcr.use_cassette
    async def test_search_paper_venue_async(self):
        data = await self.sch.search_paper('turing', venue=['ArXiv'])
        self.assertEqual(data[0].venue, 'arXiv.org')

    @test_vcr.use_cassette
    async def test_search_paper_open_access_pdf_async(self):
        data = await self.sch.search_paper('turing', open_access_pdf=True)
        self.assertTrue(data[0].openAccessPdf)

    @test_vcr.use_cassette
    async def test_search_paper_publication_date_or_year_async(self):
        date_ranges = [
            "2020-01-01",
            "2020-01",
            "2020",
            "2020-01-01:2021-01-01",
            "2020-01-01:",
            ":2020-01-01",
            "2020:2021",
            "2020:",
            ":2021",
        ]
        for date_range in date_ranges:
            with self.subTest(date_range=date_range):
                data = await self.sch.search_paper(
                    'turing', publication_date_or_year=date_range)
                self.assertTrue(len(data) > 0)

    async def test_search_paper_publication_date_or_year_invalid_async(self):
        date_ranges = [
            "2020-01-012021-01-01",
            "2020-01-01:2021-01-",
            "2020-01-01:2020-"
        ]
        for date_range in date_ranges:
            with self.subTest(date_range=date_range):
                with self.assertRaises(ValueError):
                    await self.sch.search_paper(
                        'turing', publication_date_or_year=date_range)

    @test_vcr.use_cassette
    async def test_search_paper_min_citation_count_async(self):
        data = await self.sch.search_paper('turing', min_citation_count=1000)
        self.assertTrue(all([item.citationCount >= 1000 for item in data]))

    @test_vcr.use_cassette
    async def test_search_author_async(self):
        data = await self.sch.search_author('turing')
        self.assertGreater(data.total, 0)
        self.assertEqual(data.next, 0)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_async(self):
        data = await self.sch.get_recommended_papers('10.2139/ssrn.2250500')
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_pool_from_async(self):
        data = await self.sch.get_recommended_papers(
            '10.1145/3544585.3544600', pool_from="all-cs")
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_pool_from_invalid_async(self):
        with self.assertRaises(ValueError):
            await self.sch.get_recommended_papers(
                '10.1145/3544585.3544600', pool_from="invalid")

    @test_vcr.use_cassette
    async def test_get_recommended_papers_from_lists_async(self):
        data = await self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600'], ['10.1145/301250.301271'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_from_lists_positive_only_async(self):
        data = await self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600', '10.1145/301250.301271'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_from_lists_negative_only_async(self):
        with self.assertRaises(BadQueryParametersException):
            await self.sch.get_recommended_papers_from_lists(
                [],
                ['10.1145/3544585.3544600']
            )

    @test_vcr.use_cassette
    async def test_limit_value_exceeded_async(self):
        test_cases = [
            (self.sch.get_paper_authors, '10.1093/mind/lix.236.433', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.get_paper_citations, '10.1093/mind/lix.236.433', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.get_paper_references, '10.1093/mind/lix.236.433', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.get_author_papers, 1723755, 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.search_author, 'turing', 1001,
             'The limit parameter must be between 1 and 1000 inclusive.'),
            (self.sch.search_paper, 'turing', 101,
             'The limit parameter must be between 1 and 100 inclusive.'),
            (self.sch.get_recommended_papers, '10.1145/3544585.3544600', 501,
             'The limit parameter must be between 1 and 500 inclusive.'),
            (self.sch.get_recommended_papers_from_lists,
             ['10.1145/3544585.3544600'], 501,
             'The limit parameter must be between 1 and 500 inclusive.'),
        ]
        for method, query, upper_limit, error_message in test_cases:
            with self.subTest(method=method.__name__, limit=upper_limit):
                with self.assertRaises(ValueError) as context:
                    await method(query, limit=upper_limit)
                    self.assertEqual(str(context.exception), error_message)
            with self.subTest(method=method.__name__, limit=0):
                with self.assertRaises(ValueError) as context:
                    await method(query, limit=0)
                    self.assertEqual(str(context.exception), error_message)


if __name__ == '__main__':
    unittest.main()
