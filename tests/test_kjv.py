import unittest

from hodgeys_kjv_db import kjv

class KJVTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.kjv = kjv.KJV()

    def test_fetch_books(self):
        books = self.kjv.fetch_books()
        self.assertEqual(len(books), 66)
        self.assertEqual(books[0].ShortName, 'Genesis')
        self.assertEqual(books[65].LongName, 'The Revelation of Saint John the Divine')

    def test_fetch_chapters(self):
        chapters = self.kjv.fetch_chapters(1, 1)
        self.assertEqual(len(chapters), 50)
        self.assertEqual(chapters[1], 31)

    def test_fetch_chapters_no_testament(self):
        with self.assertRaisesRegex(kjv.KJVIndexError, r"Invalid testamentId"):
            self.kjv.fetch_chapters(0, 1)

    def test_fetch_chapters_no_book(self):
        with self.assertRaisesRegex(kjv.KJVIndexError, r"Book 0 out of bounds"):
            self.kjv.fetch_chapters(1, 0)

    def test_fetch_passage(self):
        passage = self.kjv.fetch_passage(2, 4, 3, 16)
        self.assertRegex(passage.Passage1, r"3:16 For God so loved the world,")

    def test_fetch_passage_when_in_a_block(self):
        passage = self.kjv.fetch_passage(1, 1, 3, 9)
        self.assertRegex(passage.Passage1, r"(3:9).*(3:10).*")

        passage = self.kjv.fetch_passage(1, 1, 3, 10)
        self.assertRegex(passage.Passage1, r"(3:9).*(3:10).*")

    def test_fetch_passage_when_in_a_block_across_line_break(self):
        passage = self.kjv.fetch_passage(1, 1, 31, 48)
        self.assertRegex(passage.Passage1 + " " + passage.Passage2, r"(31:48).*(31:49).*")

        passage = self.kjv.fetch_passage(1, 1, 31, 49)
        self.assertRegex(passage.Passage1 + " " + passage.Passage2, r"(31:48).*(31:49).*")

    def test_fetch_passage_when_in_a_block_spanning_chapter_break(self):
        passage = self.kjv.fetch_passage(1, 18, 25, 6)
        self.assertRegex(passage.Passage1, r"(25:6).*(26:1).*(26:2).*")

        with self.assertRaisesRegex(kjv.KJVIndexError, r"Verse 7 out of bounds"):
            self.kjv.fetch_passage(1, 18, 25, 7)

        passage = self.kjv.fetch_passage(1, 18, 26, 1)
        self.assertRegex(passage.Passage1, r"(25:6).*(26:1).*(26:2).*")

        passage = self.kjv.fetch_passage(1, 18, 26, 2)
        self.assertRegex(passage.Passage1, r"(25:6).*(26:1).*(26:2).*")

    def test_fetch_passage_no_testament(self):
        with self.assertRaisesRegex(kjv.KJVIndexError, r"Invalid testamentId"):
            self.kjv.fetch_passage(99, 1, 1, 1)

    def test_fetch_passage_no_book(self):
        with self.assertRaisesRegex(kjv.KJVIndexError, r"Book 99 out of bounds"):
            self.kjv.fetch_passage(1, 99, 1, 1)

    def test_fetch_passage_no_chapter(self):
        with self.assertRaisesRegex(kjv.KJVIndexError, r"Chapter 999 out of bounds"):
            self.kjv.fetch_passage(1, 1, 999, 1)

    def test_fetch_passage_no_verse(self):
        with self.assertRaisesRegex(kjv.KJVIndexError, r"Verse 999 out of bounds"):
            self.kjv.fetch_passage(1, 1, 1, 999)

if __name__ == '__main__':
    unittest.main()
