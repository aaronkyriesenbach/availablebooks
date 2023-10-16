class Library:
    def __init__(self, name, base_url):
        self.name = name
        self.base_url = base_url


libraries = [
    Library("BPL", "https://bpl.overdrive.com/search?showOnlyAvailable=true&format=ebook-kindle&"),
    Library("Cherry Hill", "https://sjrlc.overdrive.com/search?showOnlyAvailable=true&format=ebook-kindle&"),
    Library("Northeastern", "https://northeasternuni.overdrive.com/search?showOnlyAvailable=true&format=ebook-kindle&")
]

want_to_read_url = "https://hardcover.app/@aaronkyriesenbach/books/want-to-read/airlist"
