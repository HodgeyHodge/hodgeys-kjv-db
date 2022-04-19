import unittest

from hodgeys_kjv_db import kjv


class KJVTestCase(unittest.TestCase):

    def setUp(self):
        self.kjv = kjv.KJV()

    def test_fetch_books(self):
        target = self.kjv
        result = target.fetch_books()

        self.assertTrue(len(result) == 66)
        self.assertIsInstance(result[0], kjv.Book)
        self.assertTrue(result[0].ShortName == 'Genesis')
        self.assertTrue(result[65].LongName == 'The Revelation of Saint John the Divine')
    
    def test_fetch_chapters_when_exists(self):
        target = self.kjv
        for case in [
            {'testament': 1, 'book': 1, 'testName': 'first book (old)', 'numChapters': 50, 'firstChapterNumVerses': 31},
            {'testament': 1, 'book': 39, 'testName': 'last book (old)', 'numChapters': 4, 'firstChapterNumVerses': 14},
            {'testament': 2, 'book': 1, 'testName': 'first book (new)', 'numChapters': 28, 'firstChapterNumVerses': 25},
            {'testament': 2, 'book': 27, 'testName': 'last book (new)', 'numChapters': 22, 'firstChapterNumVerses': 20}
        ]:
            with self.subTest(case=case):
                result = target.fetch_chapters(case['testament'], case['book'])

                self.assertTrue(len(result) == case['numChapters'])
                self.assertTrue(result[1] == case['firstChapterNumVerses'])
        
    def test_fetch_chapters_when_not_exists(self):
        target = self.kjv
        for case in [
            {'testament': 0, 'book': 1, 'testName': '0 testament', 'error': kjv.KJVIndexError},
            {'testament': 3, 'book': 1, 'testName': 'no such testament', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 0, 'testName': '0 book (old)', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 40, 'testName': 'no such book (old)', 'error': kjv.KJVIndexError},
            {'testament': 2, 'book': 0, 'testName': '0 book (new)', 'error': kjv.KJVIndexError},
            {'testament': 2, 'book': 28, 'testName': 'no such book (new)', 'error': kjv.KJVIndexError}
        ]:
            with self.subTest(msg=case['testName']):
                with self.assertRaises(case['error']):
                    target.fetch_chapters(case['testament'], case['book'])

    def test_fetch_passage_when_exists(self):
        target = self.kjv
        for case in [
            {'testament': 1, 'book': 1, 'chapter': 1, 'verse': 1, 'testName': 'single verse', 'attribution': '1:1', 'passage1': '1:1 In the beginning God created the heavens and the earth.', 'passage2': ''},
            {'testament': 1, 'book': 4, 'chapter': 13, 'verse': 16, 'testName': 'single verse two parts', 'attribution': '13:16', 'passage1': '13:16 These are the names of the men which Moses sent to spy out the land.', 'passage2': 'And Moses called Oshea the son of Nun Jehoshua.'},
            {'testament': 1, 'book': 1, 'chapter': 3, 'verse': 9, 'testName': 'multi verse 1/2', 'attribution': '3:9-10', 'passage1': '3:9 And the LORD God called unto Adam, and said unto him, Where art thou?  3:10 And he said, I heard thy voice in the garden, and I was afraid, because I was naked; and I hid myself.', 'passage2': ''},
            {'testament': 1, 'book': 1, 'chapter': 3, 'verse': 10, 'testName': 'multi verse 2/2', 'attribution': '3:9-10', 'passage1': '3:9 And the LORD God called unto Adam, and said unto him, Where art thou?  3:10 And he said, I heard thy voice in the garden, and I was afraid, because I was naked; and I hid myself.', 'passage2': ''},
            {'testament': 1, 'book': 1, 'chapter': 31, 'verse': 48, 'testName': 'multi verse 1/2 two parts', 'attribution': '31:48-49', 'passage1': '31:48 And Laban said, This heap is a witness between me and thee this day.', 'passage2': 'Therefore was the name of it called Galeed; 31:49 And Mizpah; for he said, The LORD watch between me and thee, when we are absent one from another.'},
            {'testament': 1, 'book': 1, 'chapter': 31, 'verse': 49, 'testName': 'multi verse 2/2 two parts', 'attribution': '31:48-49', 'passage1': '31:48 And Laban said, This heap is a witness between me and thee this day.', 'passage2': 'Therefore was the name of it called Galeed; 31:49 And Mizpah; for he said, The LORD watch between me and thee, when we are absent one from another.'},
            {'testament': 1, 'book': 18, 'chapter': 25, 'verse': 6, 'testName': 'multi chapter 1/3', 'attribution': '25:6-26:2', 'passage1': '25:6 How much less man, that is a worm? and the son of man, which is a worm?  26:1 But Job answered and said, 26:2 How hast thou helped him that is without power? how savest thou the arm that hath no strength?', 'passage2': ''},
            {'testament': 1, 'book': 18, 'chapter': 26, 'verse': 1, 'testName': 'multi chapter 2/3', 'attribution': '25:6-26:2', 'passage1': '25:6 How much less man, that is a worm? and the son of man, which is a worm?  26:1 But Job answered and said, 26:2 How hast thou helped him that is without power? how savest thou the arm that hath no strength?', 'passage2': ''},
            {'testament': 1, 'book': 18, 'chapter': 26, 'verse': 2, 'testName': 'multi chapter 3/3', 'attribution': '25:6-26:2', 'passage1': '25:6 How much less man, that is a worm? and the son of man, which is a worm?  26:1 But Job answered and said, 26:2 How hast thou helped him that is without power? how savest thou the arm that hath no strength?', 'passage2': ''},
        ]:
            with self.subTest(msg=case['testName']):
                result = target.fetch_passage(case['testament'], case['book'], case['chapter'], case['verse'])

                self.assertIsInstance(result, kjv.Passage)
                self.assertTrue(result.Testament == case['testament'])
                self.assertTrue(result.Book == case['book'])
                self.assertTrue(result.Attribution == case['attribution'])
                self.assertTrue(result.Passage1 == case['passage1'])
                self.assertTrue(result.Passage2 == case['passage2'])

    def test_fetch_passage_when_not_exists(self):
        target = self.kjv
        for case in [
            {'testament': 0, 'book': 1, 'chapter': 1, 'verse': 1, 'testName': '0 testament', 'error': kjv.KJVIndexError},
            {'testament': 3, 'book': 1, 'chapter': 1, 'verse': 1, 'testName': 'no such testament', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 0, 'chapter': 1, 'verse': 1, 'testName': '0 book', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 40, 'chapter': 1, 'verse': 1, 'testName': 'no such book', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 1, 'chapter': 0, 'verse': 1, 'testName': '0 chapter', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 1, 'chapter': 51, 'verse': 1, 'testName': 'no such chapter', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 1, 'chapter': 1, 'verse': 0, 'testName': '0 verse', 'error': kjv.KJVIndexError},
            {'testament': 1, 'book': 1, 'chapter': 1, 'verse': 32, 'testName': 'no such verse', 'error': kjv.KJVIndexError},
        ]:
            with self.subTest(msg=case['testName']):
                with self.assertRaises(case['error']):
                    target.fetch_passage(case['testament'], case['book'], case['chapter'], case['verse'])


if __name__ == '__main__':
    unittest.main()
