# deal-evaluator
A web-scraping application to compile and score private equity deals across various search sites.

# How does this application work?

This Brokered Deal Evaluator searches through business-for-sale listings on a set of websites that advertise private equity deals. To produce results, it goes through three main steps:

# 1. Finding results pages. 
For sites that use a different URL for every search result (like www.bizbuysell.com), the application first produces the relevant URL for each page of results given the state or set of states you are searching through. For sites that use a single URL for all search results (like www.sunbeltnetwork.com), this is not so simple.
Instead, for sites like this, the program uses a Python package called Selenium, which opens a phantom browser on your computer and manually enters the search terms (it types "United States" into the country field, clicks submit, clicks "Next Page", etc.) to pull up the correct listings. In either case, the program will then flip through all pages of results.

# 2. Scraping information. 
After the program has access to the results page, it can use another Python package called BeautifulSoup, which accesses a copy of the page's HTML source. This package then sorts through all of the objects on the page by tag, and pulls out the relevant information by categories and compiles a list of results.

# 3. Scoring entries. 
After the program has created this list of data, it uses another package called Pandas to organize it into a DataFrame. For each entry, the program calculates a score based on a set of positive and negative keywords—positive keywords in the title, tagline, or description earn the entry points, while negative keywords cause deductions. Finally, the Brokered Deal Evaluator produces a DataFrame with the results sorted by score. This can then be printed to a table in the application window, saved to a database, or compared to previous searches.
