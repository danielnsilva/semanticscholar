import json
import logging
import unittest
from datetime import datetime
from unittest import mock

import httpx
import vcr
from httpx import TimeoutException

from semanticscholar.AsyncSemanticScholar import AsyncSemanticScholar
from semanticscholar.Author import Author
from semanticscholar.Citation import Citation
from semanticscholar.Dataset import Dataset
from semanticscholar.DatasetDiff import DatasetDiff
from semanticscholar.Journal import Journal
from semanticscholar.Paper import Paper
from semanticscholar.PublicationVenue import PublicationVenue
from semanticscholar.Reference import Reference
from semanticscholar.Release import Release
from semanticscholar.SemanticScholar import SemanticScholar
from semanticscholar.SemanticScholarException import (
    BadQueryParametersException, GatewayTimeoutException,
    InternalServerErrorException, NoMorePagesException,
    ObjectNotFoundException, ServerErrorException)
from semanticscholar.Tldr import Tldr

test_vcr = vcr.VCR(
    cassette_library_dir='tests/data',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    record_mode=['new_episodes'],
    match_on=['uri', 'method', 'raw_body'],
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
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['name'], data['name'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    def test_release(self) -> None:
        file = open('tests/data/Release.json', encoding='utf-8')
        data = json.loads(file.read())
        release = Release(data)
        
        self.assertEqual(release.release_id, data['release_id'])
        self.assertEqual(release.readme, data['README'])
        self.assertEqual(len(release.datasets), len(data['datasets']))

        for i, dataset in enumerate(release.datasets):
            self.assertEqual(dataset.name, data['datasets'][i]['name'])
            self.assertEqual(dataset.description, data['datasets'][i]['description'])
            self.assertEqual(dataset.readme, data['datasets'][i]['README'])
        file.close()


    def test_dataset(self) -> None:
        """Test Dataset class initialization and properties."""
        file = open('tests/data/Dataset.json', encoding='utf-8')
        data = json.loads(file.read())
        dataset = Dataset(data)
        
        self.assertEqual(dataset.name, data['name'])
        self.assertEqual(dataset.description, data['description'])
        self.assertEqual(dataset.readme, data['README'])
        self.assertEqual(len(dataset.files), len(data['files']))
        for i, file_url in enumerate(dataset.files):
            self.assertEqual(file_url, data['files'][i])

        file.close()

    def test_dataset_diff(self) -> None:
        file = open('tests/data/DatasetDiff.json', encoding='utf-8')
        data = json.loads(file.read())
        dataset_diff = DatasetDiff(data)
        self.assertEqual(dataset_diff.dataset, data['dataset'])
        self.assertEqual(dataset_diff.start_release, data['start_release'])
        self.assertEqual(dataset_diff.end_release, data['end_release'])
        self.assertEqual(len(dataset_diff.diffs), len(data['diffs']))
    
        for i, diff in enumerate(dataset_diff.diffs):
            self.assertEqual(diff.from_release, data['diffs'][i]['from_release'])
            self.assertEqual(diff.to_release, data['diffs'][i]['to_release'])
            self.assertEqual(len(diff.update_files), len(data['diffs'][i]['update_files']))
            self.assertEqual(len(diff.delete_files), len(data['diffs'][i]['delete_files']))
            for j, update_file in enumerate(diff.update_files):
                self.assertEqual(update_file, data['diffs'][i]['update_files'][j])
            for j, delete_file in enumerate(diff.delete_files):
                self.assertEqual(delete_file, data['diffs'][i]['delete_files'][j])
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
        self.assertEqual(str(item.journal), str(data['journal']))
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
        self.assertEqual(str(item.tldr), str(data['tldr']))
        self.assertEqual(item.url, data['url'])
        self.assertEqual(item.venue, data['venue'])
        self.assertEqual(item.year, data['year'])
        self.assertEqual(item.raw_data, data)
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['title'], data['title'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    
    def test_paper_with_null_values_for_lists(self) -> None:
        fields = ['authors', 'citations', 'references']
        for field in fields:
            with self.subTest(field=field):
                file = open('tests/data/PaperWithNullValues.json', encoding='utf-8')
                data = json.loads(file.read())
                data = { k: v for k, v in data.items() if k == field }
                item = Paper(data)
                self.assertIsInstance(getattr(item, field), list)
                self.assertEqual(len(getattr(item, field)), 0)
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
        self.assertEqual(str(item), str(data))
        self.assertEqual(item['model'], data['model'])
        self.assertEqual(item.keys(), data.keys())
        file.close()

    @test_vcr.use_cassette
    def test_get_paper(self):
        data = self.sch.get_paper('10.1093/mind/lix.236.433', fields=['title'])
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
        data = self.sch.get_papers(list_of_paper_ids, fields=['authors'])
        for item in data:
            with self.subTest(subtest=item.paperId):
                self.assertIn(
                    'E. Duflo', [author.name for author in item.authors])

    def test_get_papers_list_size_exceeded(self):
        list_of_paper_ids = [str(i) for i in range(501)]
        self.assertRaises(ValueError, self.sch.get_papers, list_of_paper_ids)

    def test_get_papers_list_empty(self):
        list_of_paper_ids = []
        self.assertRaises(ValueError, self.sch.get_papers, list_of_paper_ids)

    @test_vcr.use_cassette
    def test_get_papers_not_found_warning(self):
        list_of_paper_ids = [
            'CorpusId:211530585',
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        with self.assertLogs(level='WARNING') as log:
            self.sch.get_papers(list_of_paper_ids)
            self.assertIn('IDs not found: [\'CorpusId:211530585\']', log.output[0])

    @test_vcr.use_cassette
    def test_get_papers_return_not_found(self):
        list_of_paper_ids = [
            'CorpusId:211530585',
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        data = self.sch.get_papers(list_of_paper_ids, return_not_found=True)
        papers = data[0]
        self.assertEqual(len(papers), 3)
        not_found = data[1]
        self.assertEqual(len(not_found), 1)
        self.assertEqual(not_found[0], 'CorpusId:211530585')

    @test_vcr.use_cassette
    def test_get_paper_authors(self):
        data = self.sch.get_paper_authors('10.2139/ssrn.2250500')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 0)
        self.assertEqual(len([item for item in data]), 4)
        self.assertEqual(data[0].name, 'E. Duflo')

    @test_vcr.use_cassette
    def test_get_paper_citations(self):
        data = self.sch.get_paper_citations(
            'CorpusID:14514057', fields=['title'])
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item.paper.title for item in data]), 1881)
        self.assertEqual(
            data[0].paper.title,
            'We\u2019ve got you covered! The effect of public health '
            'insurance on rural entrepreneurship in China')

    @test_vcr.use_cassette
    def test_get_paper_references(self):
        data = self.sch.get_paper_references(
            '10.2139/ssrn.2250500', fields=['title'], limit=50)
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 50)
        self.assertEqual(len([item for item in data]), 67)
        self.assertEqual(
            data[0].paper.title,
            'Group lending or individual lending? Evidence from a randomised '
            'field experiment in Mongolia')

    @test_vcr.use_cassette
    def test_timeout(self):
        self.sch.timeout = 0.01
        self.assertEqual(self.sch.timeout, 0.01)
        self.assertRaises(TimeoutException,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433')

    @test_vcr.use_cassette
    def test_get_author(self):
        data = self.sch.get_author(2262347, fields=['name'])
        self.assertEqual(data.name, 'A. Turing')

    @test_vcr.use_cassette
    def test_get_authors(self):
        list_of_author_ids = ['3234559', '1726629', '1711844']
        data = self.sch.get_authors(list_of_author_ids, fields=['name'])
        list_of_author_names = ['E. Dijkstra', 'D. Parnas', 'I. Sommerville']
        self.assertCountEqual(
            [item.name for item in data], list_of_author_names)

    def test_get_authors_list_size_exceeded(self):
        list_of_author_ids = [str(i) for i in range(1001)]
        self.assertRaises(ValueError, self.sch.get_authors, list_of_author_ids)

    def test_get_authors_list_empty(self):
        list_of_author_ids = []
        self.assertRaises(ValueError, self.sch.get_authors, list_of_author_ids)

    @test_vcr.use_cassette
    def test_get_authors_not_found_warning(self):
        list_of_author_ids = ['0', '3234559', '1726629', '1711844']
        with self.assertLogs(level='WARNING') as log:
            self.sch.get_authors(list_of_author_ids, fields=['name'])
            self.assertIn('IDs not found: [\'0\']', log.output[0])

    @test_vcr.use_cassette
    def test_get_authors_return_not_found(self):
        list_of_author_ids = ['0', '3234559', '1726629', '1711844']
        data = self.sch.get_authors(
            list_of_author_ids, return_not_found=True, fields=['name'])
        authors = data[0]
        self.assertEqual(len(authors), 3)
        not_found = data[1]
        self.assertEqual(len(not_found), 1)
        self.assertEqual(not_found[0], '0')

    @test_vcr.use_cassette
    def test_get_author_papers(self):
        data = self.sch.get_author_papers(1723755, limit=100, fields=['title'])
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item for item in data]), 875)
        self.assertEqual(data[0].title, 'SARS-CoV-2 hijacks p38β/MAPK11 to '
                         'promote virus replication')

    @test_vcr.use_cassette
    def test_not_found(self):
        methods = [
            [self.sch.get_paper, 'title'],
            [self.sch.get_author, 'name']
        ]
        for method, field in methods:
            with self.subTest(subtest=method.__name__):
                self.assertRaises(ObjectNotFoundException, method, 0, field)

    @test_vcr.use_cassette
    def test_bad_query_parameters(self):
        self.assertRaises(BadQueryParametersException,
                          self.sch.get_paper,
                          '10.1093/mind/lix.236.433',
                          fields=['unknown'])

    @test_vcr.use_cassette
    def test_search_paper(self):
        data = self.sch.search_paper('turing', fields=['title'])
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
        data = self.sch.search_paper('turing', fields=['title'])
        data.next_page()
        self.assertGreater(len(data), 100)

    @test_vcr.use_cassette
    def test_search_paper_traversing_results(self):
        data = self.sch.search_paper(
            'sublinear near optimal edit distance', fields=['title'])
        all_results = [item.title for item in data]
        self.assertRaises(NoMorePagesException, data.next_page)
        self.assertEqual(len(all_results), len(data.items))

    @test_vcr.use_cassette
    def test_search_paper_fields_of_study(self):
        data = self.sch.search_paper(
            'turing',
            fields_of_study=['Mathematics'],
            fields=['s2FieldsOfStudy'])
        self.assertEqual(data[0].s2FieldsOfStudy[0]['category'], 'Mathematics')

    @test_vcr.use_cassette
    def test_search_paper_year(self):
        data = self.sch.search_paper('turing', year=1936, fields=['year'])
        self.assertEqual(data[0].year, 1936)

    @test_vcr.use_cassette
    def test_search_paper_year_range(self):
        data = self.sch.search_paper(
            'turing', year='1936-1937', fields=['year'])
        self.assertTrue(all([1936 <= item.year <= 1937 for item in data]))

    @test_vcr.use_cassette
    def test_search_paper_publication_types(self):
        data = self.sch.search_paper(
            'turing',
            publication_types=['JournalArticle'],
            fields=['publicationTypes'])
        self.assertTrue('JournalArticle' in data[0].publicationTypes)
        data = self.sch.search_paper(
            'turing',
            publication_types=['Book', 'Conference'],
            fields=['publicationTypes'])
        self.assertTrue(
            'Book' in data[0].publicationTypes or
            'Conference' in data[0].publicationTypes)

    @test_vcr.use_cassette
    def test_search_paper_venue(self):
        data = self.sch.search_paper(
            'turing', venue=['ArXiv'], fields=['venue'])
        self.assertEqual(data[0].venue, 'arXiv.org')

    @test_vcr.use_cassette
    def test_search_paper_open_access_pdf(self):
        data = self.sch.search_paper(
            'turing', open_access_pdf=True, fields=['openAccessPdf'])
        self.assertTrue(data[0].openAccessPdf)

    @test_vcr.use_cassette
    def test_search_paper_publication_date_or_year(self):
        date_ranges = [
            "2024-01-01",
            "2024-01",
            "2024",
            "2024-01-01:2024-12-31",
            "2024-01-01:",
            ":2024-12-31",
            "2023:2024",
            "2023:",
            ":2024",
        ]
        for date_range in date_ranges:
            with self.subTest(date_range=date_range):
                data = self.sch.search_paper(
                    'turing',
                    publication_date_or_year=date_range,
                    fields=['title'])
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
        data = self.sch.search_paper(
            'turing', min_citation_count=1000, fields=['citationCount'])
        self.assertTrue(all([item.citationCount >= 1000 for item in data]))

    @test_vcr.use_cassette
    def test_search_paper_bulk_retrieval(self):
        data = self.sch.search_paper('kubernetes', bulk=True, fields=['title'])
        self.assertEqual(data.total, 2674)
        self.assertEqual(len(data.items), 1000)
        self.assertEqual(
            data[0].title,
            'Kubernetes Cluster for Automating Software '
            'Production Environment')

    @test_vcr.use_cassette
    def test_search_paper_bulk_retrieval_next_page(self):
        data = self.sch.search_paper('kubernetes', bulk=True, fields=['title'])
        data.next_page()
        self.assertEqual(len(data), 2000)

    @test_vcr.use_cassette
    def test_search_paper_bulk_retrieval_traversing_results(self):
        data = self.sch.search_paper('kubernetes', bulk=True, fields=['title'])
        all_results = [item.title for item in data]
        self.assertRaises(NoMorePagesException, data.next_page)
        self.assertEqual(len(all_results), len(data.items))

    @test_vcr.use_cassette
    def test_search_paper_bulk_retrieval_sorted_results_default_order(self):
        data = self.sch.search_paper(
            'kubernetes',
            bulk=True,
            sort='citationCount',
            fields=['citationCount'])
        all_data = [item.citationCount for item in data]
        self.assertTrue(sorted(all_data) == all_data)

    @test_vcr.use_cassette
    def test_search_paper_bulk_retrieval_sorted_results_asc(self):
        data = self.sch.search_paper(
            'kubernetes',
            bulk=True,
            sort='citationCount:asc',
            fields=['citationCount'])
        all_data = [item.citationCount for item in data]
        self.assertTrue(sorted(all_data) == all_data)

    @test_vcr.use_cassette
    def test_search_paper_bulk_retrieval_sorted_results_desc(self):
        data = self.sch.search_paper(
            'kubernetes',
            bulk=True,
            sort='citationCount:desc',
            fields=['citationCount'])
        all_data = [item.citationCount for item in data]
        self.assertTrue(sorted(all_data, reverse=True) == all_data)

    @test_vcr.use_cassette
    def test_search_paper_with_relevance_and_sort(self):
        with self.assertWarns(UserWarning):
            self.sch.search_paper(
                'kubernetes', sort='citationCount', fields=['title'])
    
    @test_vcr.use_cassette
    def test_search_paper_match_title(self):
        query = 'mining association rules between'
        expected_title = ('Mining association rules between sets of items in '
                          'large databases')
        paper = self.sch.search_paper(
            query, match_title=True, fields=['title'])
        self.assertEqual(paper.title, expected_title)

    def test_search_paper_match_title_and_bulk_retrieval(self):
        with self.assertRaises(ValueError):
            self.sch.search_paper('test', match_title=True, bulk=True)

    @test_vcr.use_cassette
    def test_search_author(self):
        data = self.sch.search_author('turing', fields=['name'])
        self.assertGreater(data.total, 0)
        self.assertEqual(data.next, 0)

    @test_vcr.use_cassette
    def test_get_recommended_papers(self):
        data = self.sch.get_recommended_papers(
            '10.2139/ssrn.2250500', fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_pool_from(self):
        data = self.sch.get_recommended_papers(
            '10.2139/ssrn.2250500', pool_from="all-cs", fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_pool_from_invalid(self):
        self.assertRaises(ValueError,
                          self.sch.get_recommended_papers,
                          '10.1145/3544585.3544600',
                          pool_from="invalid")

    @test_vcr.use_cassette
    def test_get_recommended_papers_from_lists(self):
        data = self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600'],
            ['10.1145/301250.301271'],
            fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_from_lists_positive_only(self):
        data = self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600', '10.1145/301250.301271'],
            fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    def test_get_recommended_papers_from_lists_negative_only(self):
        self.assertRaises(BadQueryParametersException,
                          self.sch.get_recommended_papers_from_lists,
                          [],
                          ['10.1145/3544585.3544600'],
                          fields=['title'])

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

    @test_vcr.use_cassette
    def test_empty_paginated_results(self):
        data = self.sch.search_paper('n0 r3sult s3arch t3rm', fields=['title'])
        self.assertEqual(data.total, 0)

    @test_vcr.use_cassette
    def test_debug(self):
        self.maxDiff = None
        with open('tests/data/debug_output.txt', 'r') as file:
            expected_output = file.read().strip()
        self.sch = SemanticScholar(api_key='F@k3K3y')
        list_of_paper_ids = [
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        with self.assertLogs('semanticscholar', level='DEBUG') as log, \
                self.assertRaises(PermissionError):
            self.sch.get_papers(list_of_paper_ids)
        self.assertGreater(len(log.output), 0, "Nenhum log foi capturado")
        actual_output = '\n'.join(log.output)
        self.assertEqual(actual_output, expected_output)

    @mock.patch('httpx.AsyncClient.request')
    def test_exception_internal_server_error(self, mock_request):
        mock_response = httpx.Response(
            status_code=500, json={'message': 'message'})
        mock_request.return_value = mock_response
        with self.assertRaises(InternalServerErrorException):
            self.sch.get_paper('10.1093/mind/lix.236.433')

    @mock.patch('httpx.AsyncClient.request')
    def test_exception_gateway_timeout(self, mock_request):
        mock_response = httpx.Response(
            status_code=504, json={'message': 'message'})
        mock_request.return_value = mock_response
        with self.assertRaises(GatewayTimeoutException):
            self.sch.get_paper('10.1093/mind/lix.236.433')

    @mock.patch('httpx.AsyncClient.request')
    def test_exception_server_error(self, mock_request):
        error_status = [500, 504]
        for status_code in error_status:
            mock_response = httpx.Response(
                status_code=status_code, json={'message': 'message'})
            mock_request.return_value = mock_response
            with self.assertRaises(ServerErrorException):
                self.sch.get_paper('10.1093/mind/lix.236.433')

    @test_vcr.use_cassette()
    def test_get_available_releases(self):
        releases =  self.sch.get_available_releases()
        self.assertIsInstance(releases, list)
        self.assertIsInstance(releases[0], str)
        self.assertIn('2025-08-19', releases)

    @test_vcr.use_cassette()
    def test_get_release(self):
        release_id = '2025-08-19'
        release = self.sch.get_release(release_id)

        self.assertIsInstance(release, Release)
        self.assertEqual(release.release_id, release_id)
        self.assertTrue(release.readme.startswith("Semantic Scholar Academic Graph Datasets"))
        self.assertEqual(len(release.datasets), 11)

        first_dataset = release.datasets[0]
        self.assertEqual(first_dataset.name, 'abstracts')
        self.assertTrue(first_dataset.description.startswith("Paper abstract text, where available"))
        self.assertTrue(first_dataset.readme.startswith("Semantic Scholar Academic Graph Datasets"))
        self.assertEqual(first_dataset.files, None)  # not returned as part of this call

    @test_vcr.use_cassette()
    def test_get_dataset_download_links(self):
        """
        Note: This API call requires authentication with a valid API key.
        The cassette was generated with a valid API key and then scrubbed of sensitive information.
        """
        release_id = '2025-08-19'
        dataset_name = 'papers'
        dataset = self.sch.get_dataset_download_links(release_id, dataset_name)

        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.name, dataset_name)
        self.assertTrue(dataset.description.startswith("The core attributes of a paper (title, authors, date, etc.)"))
        self.assertEqual(len(dataset.files), 30)
        self.assertTrue(dataset.files[0].startswith('https://ai2-s2ag.s3.amazonaws.com/staging/2025-08-19/papers/20250822_0'))

    @test_vcr.use_cassette()
    def test_get_dataset_diffs(self):
        """
        Note: This API call requires authentication with a valid API key.
        The cassette was generated with a valid API key and then scrubbed of sensitive information.
        """
        dataset_name = 'papers'
        start_release_id = '2024-10-08'
        end_release_id = '2025-08-19'
        diffs = self.sch.get_dataset_diffs(dataset_name, start_release_id, end_release_id)

        self.assertIsInstance(diffs, DatasetDiff)
        self.assertEqual(diffs.dataset, dataset_name)
        self.assertEqual(diffs.start_release, start_release_id)
        self.assertEqual(diffs.end_release, end_release_id)
        self.assertEqual(len(diffs.diffs), 1)

        diff = diffs.diffs[0]
        self.assertEqual(diff.from_release, '2024-10-08')
        self.assertEqual(diff.to_release, '2024-10-15')
        self.assertEqual(len(diff.update_files), 20)
        self.assertEqual(len(diff.delete_files), 4)
        self.assertEqual(diff.update_files[0], "https://ai2-s2ag.s3.amazonaws.com/updates/2024-10-08-to-2024-10-15/papers/20241018_1.gz")
        self.assertEqual(diff.delete_files[0], "https://ai2-s2ag.s3.amazonaws.com/deletes/2024-10-08-to-2024-10-15/papers/20241018_1.gz")


class AsyncSemanticScholarTest(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.sch = AsyncSemanticScholar()

    @test_vcr.use_cassette
    async def test_get_paper_async(self):
        data = await self.sch.get_paper(
            '10.1093/mind/lix.236.433', fields=['title'])
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
        data = await self.sch.get_papers(list_of_paper_ids, fields=['authors'])
        for item in data:
            with self.subTest(subtest=item.paperId):
                self.assertIn(
                    'E. Duflo', [author.name for author in item.authors])

    async def test_get_papers_list_size_exceeded_async(self):
        list_of_paper_ids = [str(i) for i in range(501)]
        with self.assertRaises(ValueError):
            await self.sch.get_papers(list_of_paper_ids)

    async def test_get_papers_list_empty_async(self):
        list_of_paper_ids = []
        with self.assertRaises(ValueError):
            await self.sch.get_papers(list_of_paper_ids)

    @test_vcr.use_cassette
    async def test_get_papers_not_found_warning_async(self):
        list_of_paper_ids = [
            'CorpusId:211530585',
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        with self.assertLogs(level='WARNING') as log:
            await self.sch.get_papers(list_of_paper_ids)
            self.assertIn('IDs not found: [\'CorpusId:211530585\']', log.output[0])

    @test_vcr.use_cassette
    async def test_get_papers_return_not_found_async(self):
        list_of_paper_ids = [
            'CorpusId:211530585',
            'CorpusId:470667',
            '10.2139/ssrn.2250500',
            '0f40b1f08821e22e859c6050916cec3667778613']
        data = await self.sch.get_papers(
            list_of_paper_ids, return_not_found=True)
        papers = data[0]
        self.assertEqual(len(papers), 3)
        not_found = data[1]
        self.assertEqual(len(not_found), 1)
        self.assertEqual(not_found[0], 'CorpusId:211530585')
    
    @test_vcr.use_cassette
    async def test_get_paper_authors_async(self):
        data = await self.sch.get_paper_authors('10.2139/ssrn.2250500')
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 0)
        self.assertEqual(len([item async for item in data]), 4)
        self.assertEqual(data[0].name, 'E. Duflo')

    @test_vcr.use_cassette
    async def test_get_paper_references_async(self):
        data = await self.sch.get_paper_references(
            '10.2139/ssrn.2250500', fields=['title'], limit=50)
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 50)
        self.assertEqual(len(data), 50)
        self.assertEqual(
            data[0].paper.title,
            'Group lending or individual lending? Evidence from a randomised '
            'field experiment in Mongolia')
    
    @test_vcr.use_cassette
    async def test_timeout_async(self):
        self.sch.timeout = 0.01
        self.assertEqual(self.sch.timeout, 0.01)
        with self.assertRaises(TimeoutException):
            await self.sch.get_paper('10.1093/mind/lix.236.433')
    
    @test_vcr.use_cassette
    async def test_get_author_async(self):
        data = await self.sch.get_author(2262347, fields=['name'])
        self.assertEqual(data.name, 'A. Turing')

    @test_vcr.use_cassette
    async def test_get_authors_async(self):
        list_of_author_ids = ['3234559', '1726629', '1711844']
        data = await self.sch.get_authors(list_of_author_ids, fields=['name'])
        list_of_author_names = ['E. Dijkstra', 'D. Parnas', 'I. Sommerville']
        self.assertCountEqual(
            [item.name for item in data], list_of_author_names)

    async def test_get_authors_list_size_exceeded_async(self):
        list_of_author_ids = [str(i) for i in range(1001)]
        with self.assertRaises(ValueError):
            await self.sch.get_authors(list_of_author_ids)

    async def test_get_authors_list_empty_async(self):
        list_of_author_ids = []
        with self.assertRaises(ValueError):
            await self.sch.get_authors(list_of_author_ids)

    @test_vcr.use_cassette
    async def test_get_authors_not_found_warning_async(self):
        list_of_author_ids = ['0', '3234559', '1726629', '1711844']
        with self.assertLogs(level='WARNING') as log:
            await self.sch.get_authors(list_of_author_ids, fields=['name'])
            self.assertIn('IDs not found: [\'0\']', log.output[0])

    @test_vcr.use_cassette
    async def test_get_authors_return_not_found_async(self):
        list_of_author_ids = ['0', '3234559', '1726629', '1711844']
        data = await self.sch.get_authors(
            list_of_author_ids, return_not_found=True, fields=['name'])
        authors = data[0]
        self.assertEqual(len(authors), 3)
        not_found = data[1]
        self.assertEqual(len(not_found), 1)
        self.assertEqual(not_found[0], '0')

    @test_vcr.use_cassette
    async def test_get_author_papers_async(self):
        data = await self.sch.get_author_papers(
            1723755, limit=100, fields=['title'])
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item async for item in data]), 875)
        self.assertEqual(
            data[0].title,
            'SARS-CoV-2 hijacks p38\u03b2/MAPK11 to promote virus replication')

    @test_vcr.use_cassette
    async def test_get_paper_citations_async(self):
        data = await self.sch.get_paper_citations(
            '10.2139/ssrn.2250500', fields=['title'])
        self.assertEqual(data.offset, 0)
        self.assertEqual(data.next, 100)
        self.assertEqual(len([item.paper.title async for item in data]), 2167)
        self.assertEqual(
            data[0].paper.title,
            'Financial inclusion and roof quality: '
            'Satellite evidence from Chilean slums')

    @test_vcr.use_cassette
    async def test_not_found_async(self):
        with self.assertRaises(ObjectNotFoundException):
            await self.sch.get_paper(0, fields=['title'])
        with self.assertRaises(ObjectNotFoundException):
            await self.sch.get_author(0, fields=['name'])

    @test_vcr.use_cassette
    async def test_bad_query_parameters_async(self):
        with self.assertRaises(BadQueryParametersException):
            await self.sch.get_paper('10.1093/mind/lix.236.433', fields=['unknown'])

    @test_vcr.use_cassette
    async def test_search_paper_async(self):
        data = await self.sch.search_paper('turing', fields=['title'])
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
        data = await self.sch.search_paper('turing', fields=['title'])
        await data.async_next_page()
        self.assertGreater(len(data), 100)

    @test_vcr.use_cassette
    async def test_search_paper_traversing_results_async(self):
        data = await self.sch.search_paper(
            'sublinear near optimal edit distance', fields=['title'])
        all_results = [item.title async for item in data]
        with self.assertRaises(NoMorePagesException):
            await data.async_next_page()
        self.assertEqual(len(all_results), len(data.items))

    @test_vcr.use_cassette
    async def test_search_paper_fields_of_study_async(self):
        data = await self.sch.search_paper(
            'turing',
            fields_of_study=['Mathematics'],
            fields=['s2FieldsOfStudy'])
        self.assertEqual(data[0].s2FieldsOfStudy[0]['category'], 'Mathematics')

    @test_vcr.use_cassette
    async def test_search_paper_year_async(self):
        data = await self.sch.search_paper(
            'turing', year=1936, fields=['year'])
        self.assertEqual(data[0].year, 1936)

    @test_vcr.use_cassette
    async def test_search_paper_year_range_async(self):
        data = await self.sch.search_paper(
            'turing', year='1936-1937', fields=['year'])
        self.assertTrue(all([1936 <= item.year <= 1937 async for item in data]))

    @test_vcr.use_cassette
    async def test_search_paper_publication_types_async(self):
        data = await self.sch.search_paper(
            'turing',
            publication_types=['JournalArticle'],
            fields=['publicationTypes'])
        self.assertTrue('JournalArticle' in data[0].publicationTypes)
        data = await self.sch.search_paper(
            'turing',
            publication_types=['Book', 'Conference'],
            fields=['publicationTypes'])
        self.assertTrue(
            'Book' in data[0].publicationTypes or
            'Conference' in data[0].publicationTypes)

    @test_vcr.use_cassette
    async def test_search_paper_venue_async(self):
        data = await self.sch.search_paper(
            'turing', venue=['ArXiv'], fields=['venue'])
        self.assertEqual(data[0].venue, 'arXiv.org')

    @test_vcr.use_cassette
    async def test_search_paper_open_access_pdf_async(self):
        data = await self.sch.search_paper(
            'turing', open_access_pdf=True, fields=['openAccessPdf'])
        self.assertTrue(data[0].openAccessPdf)

    @test_vcr.use_cassette
    async def test_search_paper_publication_date_or_year_async(self):
        date_ranges = [
            "2024-01-01",
            "2024-01",
            "2024",
            "2024-01-01:2024-12-31",
            "2024-01-01:",
            ":2024-12-31",
            "2023:2024",
            "2023:",
            ":2024",
        ]
        for date_range in date_ranges:
            with self.subTest(date_range=date_range):
                data = await self.sch.search_paper(
                    'turing',
                    publication_date_or_year=date_range,
                    fields=['title'])
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
        data = await self.sch.search_paper(
            'turing', min_citation_count=1000, fields=['citationCount'])
        self.assertTrue(all([item.citationCount >= 1000 async for item in data]))

    @test_vcr.use_cassette
    async def test_search_paper_bulk_retrieval_async(self):
        data = await self.sch.search_paper(
            'kubernetes', bulk=True, fields=['title'])
        self.assertEqual(data.total, 2674)
        self.assertEqual(len(data.items), 1000)
        self.assertEqual(
            data[0].title,
            'Kubernetes Cluster for Automating Software '
            'Production Environment')

    @test_vcr.use_cassette
    async def test_search_paper_bulk_retrieval_next_page_async(self):
        data = await self.sch.search_paper(
            'kubernetes', bulk=True, fields=['title'])
        await data.async_next_page()
        self.assertEqual(len(data), 2000)

    @test_vcr.use_cassette
    async def test_search_paper_bulk_retrieval_traversing_results_async(self):
        data = await self.sch.search_paper(
            'kubernetes', bulk=True, fields=['title'])
        all_results = [item.title async for item in data]
        print("XXX DATA", type(data))
        print(data.async_next_page)
        with self.assertRaises(NoMorePagesException):
            await data.async_next_page()
        self.assertEqual(len(all_results), len(data.items))

    @test_vcr.use_cassette
    async def test_search_paper_bulk_retrieval_sorted_results_default_order_async(self):
        data = await self.sch.search_paper(
            'kubernetes',
            bulk=True,
            sort='citationCount',
            fields=['citationCount'])
        all_data = [item.citationCount async for item in data]
        self.assertTrue(sorted(all_data) == all_data)

    @test_vcr.use_cassette
    async def test_search_paper_bulk_retrieval_sorted_results_asc_async(self):
        data = await self.sch.search_paper(
            'kubernetes',
            bulk=True,
            sort='citationCount:asc',
            fields=['citationCount'])
        all_data = [item.citationCount async for item in data]
        self.assertTrue(sorted(all_data) == all_data)

    @test_vcr.use_cassette
    async def test_search_paper_bulk_retrieval_sorted_results_desc_async(self):
        data = await self.sch.search_paper(
            'kubernetes',
            bulk=True,
            sort='citationCount:desc',
            fields=['citationCount'])
        all_data = [item.citationCount async for item in data]
        self.assertTrue(sorted(all_data, reverse=True) == all_data)

    @test_vcr.use_cassette
    async def test_search_paper_with_relevance_and_sort_async(self):
        with self.assertWarns(UserWarning):
            await self.sch.search_paper(
                'kubernetes', sort='citationCount', fields=['title'])

    @test_vcr.use_cassette
    async def test_search_paper_match_title_async(self):
        query = 'mining association rules between'
        expected_title = ('Mining association rules between sets of items in '
                          'large databases')
        paper = await self.sch.search_paper(
            query, match_title=True, fields=['title'])
        self.assertEqual(paper.title, expected_title)

    async def test_search_paper_match_title_and_bulk_retrieval_async(self):
        with self.assertRaises(ValueError):
            await self.sch.search_paper('test', match_title=True, bulk=True)

    @test_vcr.use_cassette
    async def test_search_author_async(self):
        data = await self.sch.search_author('turing', fields=['name'])
        self.assertGreater(data.total, 0)
        self.assertEqual(data.next, 0)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_async(self):
        data = await self.sch.get_recommended_papers(
            '10.2139/ssrn.2250500', fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_pool_from_async(self):
        data = await self.sch.get_recommended_papers(
            '10.2139/ssrn.2250500', pool_from="all-cs", fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_pool_from_invalid_async(self):
        with self.assertRaises(ValueError):
            await self.sch.get_recommended_papers(
                '10.1145/3544585.3544600', pool_from="invalid")

    @test_vcr.use_cassette
    async def test_get_recommended_papers_from_lists_async(self):
        data = await self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600'],
            ['10.1145/301250.301271'],
            fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_from_lists_positive_only_async(self):
        data = await self.sch.get_recommended_papers_from_lists(
            ['10.1145/3544585.3544600', '10.1145/301250.301271'],
            fields=['title'])
        self.assertEqual(len(data), 100)

    @test_vcr.use_cassette
    async def test_get_recommended_papers_from_lists_negative_only_async(self):
        with self.assertRaises(BadQueryParametersException):
            await self.sch.get_recommended_papers_from_lists(
                [],
                ['10.1145/3544585.3544600'],
                fields=['title'])

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

    @mock.patch('httpx.AsyncClient.request')
    async def test_exception_internal_server_error_async(self, mock_request):
        mock_response = httpx.Response(
            status_code=500, json={'message': 'message'})
        mock_request.return_value = mock_response
        with self.assertRaises(InternalServerErrorException):
            await self.sch.get_paper('10.1093/mind/lix.236.433')

    @mock.patch('httpx.AsyncClient.request')
    async def test_exception_gateway_timeout_async(self, mock_request):
        mock_response = httpx.Response(
            status_code=504, json={'message': 'message'})
        mock_request.return_value = mock_response
        with self.assertRaises(GatewayTimeoutException):
            await self.sch.get_paper('10.1093/mind/lix.236.433')

    @mock.patch('httpx.AsyncClient.request')
    async def test_exception_server_error_async(self, mock_request):
        error_status = [500, 504]
        for status_code in error_status:
            mock_response = httpx.Response(
                status_code=status_code, json={'message': 'message'})
            mock_request.return_value = mock_response
            with self.assertRaises(ServerErrorException):
                await self.sch.get_paper('10.1093/mind/lix.236.433')


    @test_vcr.use_cassette()
    async def test_get_available_releases(self):
        releases =  await self.sch.get_available_releases()
        self.assertIsInstance(releases, list)
        self.assertIsInstance(releases[0], str)
        self.assertIn('2025-08-19', releases)

    @test_vcr.use_cassette()
    async def test_get_release(self):
        release_id = '2025-08-19'
        release = await self.sch.get_release(release_id)

        self.assertIsInstance(release, Release)
        self.assertEqual(release.release_id, release_id)
        self.assertTrue(release.readme.startswith("Semantic Scholar Academic Graph Datasets"))
        self.assertEqual(len(release.datasets), 11)

        first_dataset = release.datasets[0]
        self.assertEqual(first_dataset.name, 'abstracts')
        self.assertTrue(first_dataset.description.startswith("Paper abstract text, where available"))
        self.assertTrue(first_dataset.readme.startswith("Semantic Scholar Academic Graph Datasets"))
        self.assertEqual(first_dataset.files, None)  # not returned as part of this call

    @test_vcr.use_cassette()
    async def test_get_dataset_download_links(self):
        """
        Note: This API call requires authentication with a valid API key.
        The cassette was generated with a valid API key and then scrubbed of sensitive information.
        """
        release_id = '2025-08-19'
        dataset_name = 'papers'
        dataset = await self.sch.get_dataset_download_links(release_id, dataset_name)

        self.assertIsInstance(dataset, Dataset)
        self.assertEqual(dataset.name, dataset_name)
        self.assertTrue(dataset.description.startswith("The core attributes of a paper (title, authors, date, etc.)"))
        self.assertEqual(len(dataset.files), 30)
        self.assertTrue(dataset.files[0].startswith('https://ai2-s2ag.s3.amazonaws.com/staging/2025-08-19/papers/20250822_0'))

    @test_vcr.use_cassette()
    async def test_get_dataset_diffs(self):
        """
        Note: This API call requires authentication with a valid API key.
        The cassette was generated with a valid API key and then scrubbed of sensitive information.
        """
        dataset_name = 'papers'
        start_release_id = '2024-10-08'
        end_release_id = '2025-08-19'
        diffs = await self.sch.get_dataset_diffs(dataset_name, start_release_id, end_release_id)

        self.assertIsInstance(diffs, DatasetDiff)
        self.assertEqual(diffs.dataset, dataset_name)
        self.assertEqual(diffs.start_release, start_release_id)
        self.assertEqual(diffs.end_release, end_release_id)
        self.assertEqual(len(diffs.diffs), 1)

        diff = diffs.diffs[0]
        self.assertEqual(diff.from_release, '2024-10-08')
        self.assertEqual(diff.to_release, '2024-10-15')
        self.assertEqual(len(diff.update_files), 20)
        self.assertEqual(len(diff.delete_files), 4)
        self.assertEqual(diff.update_files[0], "https://ai2-s2ag.s3.amazonaws.com/updates/2024-10-08-to-2024-10-15/papers/20241018_1.gz")
        self.assertEqual(diff.delete_files[0], "https://ai2-s2ag.s3.amazonaws.com/deletes/2024-10-08-to-2024-10-15/papers/20241018_1.gz")

if __name__ == '__main__':
    unittest.main()
