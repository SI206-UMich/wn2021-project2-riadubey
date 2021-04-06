Ria Dubey 
uniquename: riadubey
Partner: Meera Amin

rom bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

#  

def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    answ = []
    with open(filename) as f:
        f = f.read()

        soup = BeautifulSoup(f, 'html.parser')

        # Get all titles + authors
        atags_title = soup.find_all('a', class_="bookTitle")
        # atags_author = soup.find_all('a', class_="bookTitle")
        for a in atags_title:

            title = str(a.span.string).strip()
            # import pdb;
            # pdb.set_trace() 
            auth = a.parent.find('a', class_="authorName")
            author = str(auth.span.string).strip()
            answ.append((title, author))
            
        # print(answ)
        return answ
    return answ



def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    r = requests.get("https://www.goodreads.com/genres/fantasy")
    soup = BeautifulSoup(r.text, 'html.parser')
    new_releases = soup.find_all(class_ = "coverWrapper")
    all_URLS = []
    for book in new_releases:
        if len(all_URLS) < 15: 
            url = book.find('a')
            all_URLS.append("https://www.goodreads.com" + url["href"])
    return all_URLS


def get_book_summary(book_url):
    # print(book_url)
    req  = requests.get(book_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    # import pdb; pdb.set_trace()
    title = str(soup.find('h1', id="bookTitle").string).strip()
    author = str(soup.find('a', class_="authorName").span.string).strip()
    pages = int(str(soup.find('span', {"itemprop":"numberOfPages"}).string).strip().split()[0])

    return (title,author,pages)


    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """



def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """

    file = open(filepath)
    f = file.read()
    summaries = []
    soup = BeautifulSoup(f, 'html.parser')
    fix = {}

    for item in soup.findAll('div', {'class': 'category clearFix'}):
        cat = item.find('a').find('h4').text.strip()
        title = item.find('img', {"class": "category__winnerImage"}).get('alt').strip()
        url = item.find('a').get('href').replace('\n', '')
        summaries.append((str(cat), str(title), str(url)))
    return summaries 
    


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Book Title','Author Name']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        csv_writer.writeheader()
        for i in data:
            csv_writer.writerow({'Book Title': i[0],'Author Name':i[1]})


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles = get_titles_from_search_results("search_results.htm")

        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(titles), list)

        # check that each item in the list is a tuple
        for title in titles:
            self.assertEqual(type(title), tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles[0][0], "Harry Potter and the Deathly Hallows (Harry Potter, #7)" )
        self.assertEqual(titles[0][1], "J.K. Rowling" )

        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles[-1][0], "Harry Potter: The Prequel (Harry Potter, #0.5)")
        self.assertEqual(titles[-1][1], "J.K. Rowling" )


    def test_get_search_links(self):
        # urls = get_search_links()

        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)

        # check that each URL in the TestCases.search_urls is a string
        for el in TestCases.search_urls:
            self.assertEqual(type(el), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for el in TestCases.search_urls:
            self.assertTrue("https://www.goodreads.com/book/show/" in el)
        


    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summ = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for url in TestCases.search_urls:
            summ.append(get_book_summary(url))
        
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summ), 10)

        for el in summ:


            # check that each item in the list is a tuple
            self.assertEqual(type(el), tuple)

            # check that each tuple has 3 elements
            self.assertEqual(len(el), 3)

            # check that the first two elements in the tuple are string
            self.assertEqual(type((el)[0]), str )
            self.assertEqual(type((el)[1]), str )

            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type((el)[2]), int )
    
        # check that the first book in the search has 337 pages
        self.assertEqual(summ[0][2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summ = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(summ), 20)

        for el in summ:
            # assert each item in the list of best books is a tuple
            self.assertEqual(type(el), tuple)
    
            # check that each tuple has a length of 3
            self.assertEqual(len(el), 3)

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summ[0], ('Fiction', "The Midnight Library", "https://www.goodreads.com/choiceawards/best-fiction-books-2020"))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summ[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles, "test.csv")
        
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv') as infile:
            csvlines = infile.readlines()

            # check that there are 21 lines in the csv
            self.assertEqual(len(csvlines), 21)


            # check that the header row is correct
            self.assertEqual(csvlines[0].strip(), "Book Title,Author Name")

            # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
            self.assertEqual(csvlines[1].strip(), '"Harry Potter and the Deathly Hallows (Harry Potter, #7)",J.K. Rowling')


            # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
            self.assertEqual(csvlines[-1].strip(), '"Harry Potter: The Prequel (Harry Potter, #0.5)",J.K. Rowling')



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



