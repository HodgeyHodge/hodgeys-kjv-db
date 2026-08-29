import unittest

from hodgeys_kjv_db.database import DEFAULT_DB_PATH, get_db_cursor

class DBTestCase(unittest.TestCase):

    def db_cursor(self, factory=None):
        return get_db_cursor(db_path=DEFAULT_DB_PATH, factory=factory)

    def test_chapter_count(self):
        query = "SELECT SUM(NumChapters) FROM BookStats;"
        with self.db_cursor() as cur:
            res = cur.execute(query)
            total_chapters = res.fetchone()[0]
            self.assertEqual(total_chapters, 1189)

    def test_chapter_count_2(self):
        query = "SELECT COUNT(*) FROM ChapterStats;"
        with self.db_cursor() as cur:
            res = cur.execute(query)
            total_chapters = res.fetchone()[0]
            self.assertEqual(total_chapters, 1189)

    def test_OT_verse_count(self):
        query = "SELECT SUM(NumVerses) FROM ChapterStats WHERE TestamentID = 1;"
        with self.db_cursor() as cur:
            res = cur.execute(query)
            ot_verse_count = res.fetchone()[0]
            self.assertEqual(ot_verse_count, 23145)

    def test_NT_verse_count(self):
        query = "SELECT SUM(NumVerses) FROM ChapterStats WHERE TestamentID = 2;"
        with self.db_cursor() as cur:
            res = cur.execute(query)
            nt_verse_count = res.fetchone()[0]
            self.assertEqual(nt_verse_count, 7957)

if __name__ == '__main__':
    unittest.main()
