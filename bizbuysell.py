from score import score as Score
import time
try:
    import bs4 as bs
    import pandas as pd
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
except ImportError:
    import install_requirements
    import bs4 as bs
    import pandas as pd
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options

def soupify(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 \
        Safari/537.36'}
    source = requests.get(url, headers=headers)
    soup = bs.BeautifulSoup(source.content, 'lxml')
    return soup

states_list = ("All", "Alabama", "Alaska", "Arizona", "Arkansas", "California", \
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", \
    "Idaho","Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", \
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", \
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", \
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", \
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", \
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", \
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", \
    "West Virginia", "Wisconsin", "Wyoming", "All")

class BizBuySell():
    def __init__(self, states, page=1, settings=None, positive_inputs=None, \
        negative_inputs=None):
        """Settings is a dictionary with optional search settings
        for the website, in Category: Setting pairs.
        """
        
        self.state = states[0]
        if not isinstance(self.state, str):
            raise TypeError("State must be a string.")
        elif self.state.title() not in states_list:
            raise ValueError("State must be a U.S. state or 'All'.")

        self.other_states = states[1:]
        for state in self.other_states:
            if not isinstance(state, str):
                raise TypeError("Every state must be a string.")
            elif state.title() not in states_list:
                raise ValueError("Every state must be a U.S. state.")
        
        self.page = page
        if not isinstance(page, int):
            raise TypeError("Page must be an integer.")
        self.settings = settings
        
        self.url = self.find_url()
        self.soup = soupify(self.url)
        self.positive_inputs = positive_inputs
        self.negative_inputs = negative_inputs

    def __len__(self):
        return len(self.concat_states()[0])

    def __repr__(self):
        if self.state.lower() == "all":
            return "BizBuySell.com Listings for All U.S. States"
        else:
            states_here = ", ".join(self.other_states)
            full_states = ", ".join([states_here, self.state])
            return f"BizBuySell.com Listings for {full_states}"

    def __str__(self):
        states_here = ", ".join(self.other_states)
        full_states = ", ".join([states_here, self.state])
        return f"""BizBuySell.com Listings for States: {full_states}
        Number of results: {self.__len__()}
        """

    def __add__(self, other):
        df = self.make_dataframe()
        if isinstance(other.make_dataframe(), pd.DataFrame):
            new_df = pd.concat([df, other.make_dataframe()], \
                ignore_index=True, verify_integrity=True)
            return new_df.sort_values(by=["Score"])
        elif isinstance(other, pd.DataFrame):
            new_df = pd.concat([df, other], ignore_index=True, \
                verify_integrity=True)
            return new_df.sort_values(by=["Score"], ascending=False)
        else:
            raise TypeError("Cannot concatenate with non-DataFrames.")

    def find_url(self):
        start = "https://www.bizbuysell.com/"
        lower_name = self.state.lower().replace(" ", "-")
        loc = "" if lower_name == "all" else lower_name + "-"

        if self.settings is not None:
            search_url = start + "buy/"
            op = webdriver.ChromeOptions()
            #op.add_argument("headless")
            op.add_argument("window-size=1200x600")
            driver = webdriver.Chrome(options=op)
            driver.get(search_url)

            #categories = driver.find_element_by_class_name("modalMenu")
            categories = driver.find_element_by_partial_link_text("Select Categories")
            categories.click()
            time.sleep(2)

            for cat in self.settings["categories"]:
                button = driver.find_element_by_partial_link_text(cat)
                button.click()
            driver.find_element_by_partial_link_text("Save Changes").click()

            if "price_min" in self.settings or "price_max" in self.settings:
                pr_label = "ctl00_Content_ctl00DisplayPriceRange"
                driver.find_element_by_id(pr_label).click()
                if "price_min" in self.settings:
                    price = self.settings["price_min"]
                    x = f"//a[@class='minOption' and text()='{price}']"
                    driver.find_element_by_xpath(x).click()
                if "price_max" in self.settingg:
                    price = self.settings["price_max"]
                    x = f"//a[@class='maxOption' and text()='{price}']"
                    driver.find_element_by_xpath(x).click()

            if "cf_min" in self.settings or "cf_max" in self.settings:
                cf_label = "ctl00_Content_ctl00DisplayCashFlow"
                driver.find_element_by_id(cf_label).click()
                if "cf_min" in self.settings:
                    cf = self.settings["cf_min"]
                    x = f"//a[@class='minOption' and text()='{cf}']"
                    driver.find_element_by_xpath(x).click()
                if "cf_max" in self.settingg:
                    cf = self.settings["cf_max"]
                    x = f"//a[@class='maxOption' and text()='{cf}']"
                    driver.find_element_by_xpath(x).click()
            
            js_tag = "javascript:document.ebsearch.submit();"
            driver.find_element_by_xpath(f"//a[@href='{js_tag}']")

            url = driver.current_url
            ending = url[url.find("?"):]

        else:
            ending = "?q=Y2Zmcm9tPTc1MDAwMCZjZnRvPTMwMDAwMDAmaT05OVlCJmlyPTEmc3BpZD00"

        page_no_str = "" if self.page == 1 else str(self.page) + "/"
        middle = "businesses-for-sale/"
        return start + loc + middle + page_no_str + ending

    def count_pages(self):
        b = '</span></li><li><a href="https://www.bizbuysell.com/businesses-for-sale/'
        index = str(self.soup).find(b) + len(b)
        last_page = str(self.soup)[index:index + 1]
        return int(last_page) if last_page != " " else 1

    def scrape_titles(self):
        mydivs = self.soup.findAll("b", {"class": \
            "title hidden-desktop hidden-tablet"})
        titles = [div.get_text().replace("&amp;", "&") for div in mydivs]
        return titles

    def scrape_urls(self):
        urls = []
        for link in self.soup.find_all("a", {"class": \
            ["listingResult result diamond", \
            "listingResult result featured", \
            "listingResult result featured swiper", \
            "listingResult result basic"]}):
            url = str(link.get("href"))
            if url[:9].lower() == "/business":
                url = "https://www.bizbuysell.com" + url
            urls.append(url)
        return urls

    def scrape_taglines(self):
        mydivs = self.soup.findAll("i", {"class": \
            "tagline hidden-desktop hidden-tablet"})
        taglines = [div.get_text().replace("&amp;","&") for div in mydivs]
        return taglines

    def scrape_cashflows(self):
        mydivs = self.soup.findAll("span", {"class": "cflow hidden-phone"})
        cashflows = [div.get_text()[11:] for div in mydivs]
        return cashflows

    def scrape_descriptions(self):
        mydivs = self.soup.findAll("p", {"class": ["desc", "desc financing"]})
        descriptions = [div.get_text().replace("&amp;","&") for div in mydivs]
        # First description on State Page is Broker's phone number
        return descriptions if self.state == "All" else descriptions[1:]

    def scour(self):
        """Returns a full list of results, categorized in sublists."""

        master_list = [self.scrape_titles(), self.scrape_taglines(), \
            self.scrape_cashflows(), self.scrape_descriptions(), [], \
            self.scrape_urls()]

        # Let's first ensure all vectors are the same length
        # If Taglines too short, it's because basic listings have no TL
        difference = len(master_list[0]) - len(master_list[1])
        if (len(master_list[0]) == len(master_list[2]) and difference):
            master_list[1].extend(["(No Tagline)" for i in range(difference)])

        if self.positive_inputs is None and self.negative_inputs is None:
            for i, desc in enumerate(master_list[3]):
                master_list[4].append(Score(" ".join([master_list[0][i], \
                    master_list[1][i], desc])))
        else:
            for i, desc in enumerate(master_list[3]):
                master_list[4].append(Score(" ".join([master_list[0][i], \
                    master_list[1][i], desc]), \
                    positive_inputs=self.positive_inputs, \
                    negative_inputs=self.negative_inputs))

        return master_list

    def concat_pages(self, no_pages=-1):
        """Returns a list of each column in a sublist, across pages.
        If Kwarg no_pages = -1, we search all pages.
        Otherwise, Kwarg is the number of pages to search.
        """

        if no_pages == -1:
            last_page = self.count_pages()
        elif isinstance(no_pages, int):
            last_page = no_pages
        else:
            raise TypeError("No_pages must be an Integer.")

        master_list = self.scour()
        for page in range(2, last_page + 1):
            current_scour = BizBuySell([self.state], page).scour()
            for entry in range(len(current_scour[0])):
                for idx, list_ in enumerate(master_list):
                    list_.append(current_scour[idx][entry])

        return master_list

    def concat_states(self):
        """Combines the entries from different states. Returns a list 
        of each column in a sublist, across pages and states.
        """
        
        master_list = self.concat_pages()
        for state in self.other_states:
            current_scour = BizBuySell([state]).scour()
            for entry in range(len(current_scour[0])):
                for idx, list_ in enumerate(master_list):
                    list_.append(current_scour[idx][entry])

        return master_list

    def make_dataframe(self):
        """Turns concatenated pages data into DF sorted by score."""

        master_list = self.concat_states()
        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL")

        df = pd.DataFrame(dict(zip(cols, master_list)), columns=cols)
        df_sorted = df.sort_values(by=["Score"], ascending=False)
        return df_sorted


if __name__ == "__main__":
    state_inputs = input("Which states should we check? \n")
    inputs = [state.strip() for state in state_inputs.split(",")]
    start_time = time.time()
    case = BizBuySell(inputs)

    print("\nScraping BizBuySell.com...\n", end='')

    try:
        df_sorted = case.make_dataframe()
        print(df_sorted)
        print(f"\nCompleted in {time.time() - start_time}s.\n")
    except ValueError:
        print("Columns might be different sizes:")
        cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
            "Score", "URL")
        for i, col in enumerate(cols):
            print(f"{col}: {len(case.scour()[i])}")