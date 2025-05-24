# lib/classes/many_to_many.py

class Article:
    all = []

    def __init__(self, author, magazine, title):
        # validate types
        if not isinstance(author, Author):
            raise TypeError("author must be an Author instance")
        if not isinstance(magazine, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if not (5 <= len(title) <= 50):
            raise ValueError("title length must be between 5 and 50 characters")

        # assign properties
        self.author = author
        self.magazine = magazine
        self._title = title

        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # immutable: ignore any reassignment
        return

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise TypeError("author must be an Author instance")
        self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            raise TypeError("magazine must be a Magazine instance")
        self._magazine = value


class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) == 0:
            raise ValueError("name cannot be empty")
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # immutable: ignore any reassignment
        return

    def articles(self):
        """All Article instances written by this author."""
        return [a for a in Article.all if a.author is self]

    def magazines(self):
        """Unique list of Magazine instances this author has written for."""
        return list({a.magazine for a in self.articles()})

    def add_article(self, magazine, title):
        """Creates & returns a new Article tied to this author."""
        return Article(self, magazine, title)

    def topic_areas(self):
        """Unique list of magazine categories this author writes in, or None."""
        mags = self.magazines()
        if not mags:
            return None
        return list({m.category for m in mags})


class Magazine:
    _all = []

    def __init__(self, name, category):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not (2 <= len(name) <= 16):
            raise ValueError("name length must be between 2 and 16 characters")
        if not isinstance(category, str):
            raise TypeError("category must be a string")
        if len(category) == 0:
            raise ValueError("category cannot be empty")

        self._name = name
        self._category = category
        Magazine._all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # allow change only if valid string length 2–16; else ignore
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        return

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # allow change only if valid non-empty string; else ignore
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        return

    def articles(self):
        """All Article instances published in this magazine."""
        return [a for a in Article.all if a.magazine is self]

    def contributors(self):
        """Unique list of Authors who have written for this magazine."""
        return list({a.author for a in self.articles()})

    def article_titles(self):
        """List of titles in this magazine, or None if empty."""
        titles = [a.title for a in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        """
        Authors with more than 2 articles in this magazine,
        or None if no one qualifies.
        """
        counts = {}
        for art in self.articles():
            counts[art.author] = counts.get(art.author, 0) + 1
        result = [auth for auth, cnt in counts.items() if cnt > 2]
        return result if result else None

    @classmethod
    def top_publisher(cls):
        """
        Magazine with the most articles overall,
        or None if there are no articles.
        """
        if not Article.all:
            return None
        return max(cls._all, key=lambda mag: len(mag.articles()))
