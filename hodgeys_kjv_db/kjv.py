from typing import NamedTuple
from enum import Enum

from .database import DEFAULT_DB_PATH, get_db_cursor
from .exceptions import *

class KJV:
    """Instantiate the wrapper."""

    def __init__(self, datapath=None, connection=None):
        self.datapath = datapath or DEFAULT_DB_PATH
        self.connection = connection

    def _cursor(self, factory=None):
        return get_db_cursor(
            db_path=self.datapath,
            factory=factory,
            connection=self.connection,
        )

    def fetch_books(self):
        """Get every book, as a list of Book objects."""
        query = """
            SELECT
                b.TestamentID,
                b.BookID,
                b.ShortName,
                b.LongName,
                bs.NumChapters
            FROM
                Books b
            JOIN
                BookStats bs ON b.TestamentID = bs.TestamentID AND b.BookId = bs.BookId;
        """
        with self._cursor() as cur:
            cur.execute(query)
            return [Book(*row) for row in cur.fetchall()]
    
    def fetch_chapters(self, testamentId: int, bookId: int):
        """Get a dict of chapter lengths for the given book."""
        self._validate_coordinates(testamentId, bookId)

        query = f"""
            SELECT
                c.ChapterID,
                c.NumVerses
            FROM
                ChapterStats c
            WHERE
                c.TestamentID = ? AND
                c.BookID = ?
        """
        params = (testamentId, bookId)

        with self._cursor() as cur:
            cur.execute(query, (testamentId, bookId))
            rows = cur.fetchall()
            if not rows:
                raise KJVIndexError(
                    f"Book not found: testamentId {testamentId}, bookId {bookId}"
                )
            return {row[0]: row[1] for row in rows}

    def fetch_passage(self, testamentId: int, bookId: int, chapterId: int, verseId: int):
        """Get a Passage object, since some verses come pre-joined in compound passages."""
        self._validate_coordinates(testamentId, bookId, chapterId, verseId)

        query = """
            SELECT Index_, Passage1, Passage2
            FROM Bible
            WHERE TestamentID = ? AND BookID = ?
              AND (
                (ChapterID = ? AND EndChapter = ? AND VerseID <= ? AND EndVerse >= ?) OR
                (ChapterID = ? AND EndChapter = ChapterId + 1 AND VerseID <= ?) OR
                (ChapterID + 1 = EndChapter AND EndChapter = ? AND 1 <= ? AND EndVerse >= ?)
              );
        """
        params = (
            testamentId,
            bookId,
            chapterId,
            chapterId,
            verseId,
            verseId,
            chapterId,
            verseId,
            chapterId,
            verseId,
            verseId
        )

        with self._cursor() as cur:
            cur.execute(query, params)
            row = cur.fetchone()
            if not row:
                raise KJVIndexError(
                    f"Passage not found: testamentId {testamentId}, bookId {bookId}, "
                    f"chapterId {chapterId}, verseId {verseId}"
                )
            return Passage(testamentId, bookId, *row)

    def _validate_coordinates(
        self,
        testamentId: int,
        bookId: int,
        chapterId: int = None,
        verseId: int = None,
    ):
        """Validate that Testament, Book, Chapter, and Verse exist."""
        if testamentId not in (1, 2):
            raise KJVIndexError(f"Invalid testamentId: {testamentId}. Must be 1 (OT) or 2 (NT).")
    
        query = "SELECT NumChapters FROM BookStats WHERE TestamentID = ? AND BookID = ?;"

        with self._cursor() as cur:
            cur.execute(query, (testamentId, bookId))
            row = cur.fetchone()
    
        if not row:
            raise KJVIndexError(f"Book {bookId} out of bounds for {('OT' if testamentId == 1 else 'NT')}")
        maxChapters = row[0]

        if chapterId is not None:
            if chapterId < 1 or chapterId > maxChapters:
                raise KJVIndexError(
                    f"Chapter {chapterId} out of bounds for {('OT' if testamentId == 1 else 'NT')}, Book {bookId}. "
                    f"Valid chapters: 1-{maxChapters}."
                )
    
        if verseId is not None:
            query = "SELECT NumVerses FROM ChapterStats WHERE TestamentID = ? AND BookID = ? AND ChapterID = ?;"

            with self._cursor() as cur:
                cur.execute(query, (testamentId, bookId, chapterId))
                row = cur.fetchone()

            if not row:
                raise KJVError("Data corrupt!")
            maxVerses = row[0]

            if verseId < 1 or verseId > maxVerses:
                raise KJVIndexError(
                    f"Verse {verseId} out of bounds for {('OT' if testamentId == 1 else 'NT')}, Book {bookId}, Chapter {chapterId}. "
                    f"Valid verses: 1-{maxVerses}."
                )

class Book(NamedTuple):
    Testament: int
    Book: int
    ShortName: str
    LongName: str
    ChapterCount: int

class Passage(NamedTuple):
    Testament: int
    Book: int
    Attribution: str
    Passage1: str
    Passage2: str
