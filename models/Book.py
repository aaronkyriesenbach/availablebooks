class Book:
    def __init__(self, title, author=None):
        self.title = title
        self.author = author

    def __str__(self):
        if self.author is not None:
            return f"{self.title} by {self.author}"
        else:
            return self.title