from score import score as Score
import time
try:
    import bs4 as bs
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
except ImportError:
    import install_requirements
    import bs4 as bs
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options

states_list = ("Alabama", "Alaska", "Arizona", "Arkansas", "California", \
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", \
    "Idaho","Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", \
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", \
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", \
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", \
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", \
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", \
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", \
    "West Virginia", "Wisconsin", "Wyoming", "All")
    
class Sunbelt():
    def __init__(self, states, mode="headless", settings=None, \
        positive_inputs=None, negative_inputs=None):
        """Mode is either "headless" for no window popping up,
        or "show" if you want to watch the browser run.
        """

        if not isinstance(states, list):
            raise TypeError("States must be in a list.")

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

        self.mode = mode
        if self.mode == "headless":
            op = webdriver.ChromeOptions()
            op.add_argument("headless")
            op.add_argument("window-size=1200x600")
            self.driver = webdriver.Chrome(options=op)
        elif self.mode == "show":
            self.driver = webdriver.Chrome("chromedriver")
        else:
            raise ValueError("Mode must be either 'headless' or 'show'.")
        
        self.settings = settings
        self.soup = self.soupify()
        self.positive_inputs = positive_inputs
        self.negative_inputs = negative_inputs

    def __len__(self):
        return len(self.concat_states()[0])

    def __repr__(self):
        if self.state.lower() == "all":
            return "SunbeltNetwork.com Listings for All U.S. States"
        else:
            states_here = ", ".join(self.other_states)
            full_states = ", ".join([states_here, self.state])
            return f"SunbeltNetwork.com Listings for {full_states}"

    def __str__(self):
        states_here = ", ".join(self.other_states)
        full_states = ", ".join([states_here, self.state])
        return f"""SunbeltNetwork.com Listings for States: {full_states}
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

    def soupify(self, occurance="first"):
        """Opens the webpage and finds search results."""

        driver = self.driver
        if occurance == "first":
            driver.get("https://www.sunbeltnetwork.com/business-search/business-results/")
            country = driver.find_element_by_name("country")
            country.send_keys("United States")
            state = driver.find_element_by_name("state")
            state.send_keys(self.state)

            if self.settings is not None:
                cats = self.settings["categories"]

                if cats != ["All Categories"]:
                    for cat in cats:
                        x = f"//option[text()='{cat}']"
                        element = driver.find_element_by_xpath(x)
                        element.click()
                    element.submit()

                if "price_min" in self.settings:
                    price = self.settings["price_min"]
                    element = driver.find_element_by_name("price-min")
                    element.click()
                    element.send_keys(price)
                    element.submit()

                if "price_max" in self.settingg:
                    price = self.settings["price_max"]
                    element = driver.find_element_by_name("price-max")
                    element.click()
                    element.send_keys(price)
                    element.submit()

                if "revenue_min" in self.settings:
                    revenue = self.settings["revenue_min"]
                    element = driver.find_element_by_name("revenue-min")
                    element.click()
                    element.send_keys(revenue)
                    element.submit()

                if "revenue_max" in self.settingg:
                    revenue = self.settings["revenue_max"]
                    element = driver.find_element_by_name("revenue-max")
                    element.click()
                    element.send_keys(revenue)
                    element.submit()

                if "cf_min" in self.settings:
                    cf = self.settings["cf_min"]
                    element = driver.find_element_by_name("cf-min")
                    element.click()
                    element.send_keys(cf)
                    element.submit()

                if "cf_max" in self.settingg:
                    cf = self.settings["cf_max"]
                    element = driver.find_element_by_name("cf-max")
                    element.click()
                    element.send_keys(cf)
                    element.submit()

            else:
                cf = driver.find_element_by_name("cf-min")
                cf.send_keys("750000")
                cf2 = driver.find_element_by_name("cf-max")
                cf2.send_keys("3000000")
                cf2.submit()

            time.sleep(1)

        elif occurance == "next":
            next_button = driver.find_element_by_partial_link_text("NEXT")
            next_button.click()
            time.sleep(1)
        else:
            raise ValueError("Occurance must be 'first' or 'next'.")

        soup = bs.BeautifulSoup(driver.page_source, "lxml")
        if " 0 businesses and companies for sale in" in str(soup):
            print("No businesses found.")
        return soup

    def count_pages(self):
        try:
            results = self.soup.find_all("span", \
                attrs={"class": "page-link"})
            page_nos = [h3.get_text() for h3 in results]
            return int(page_nos[-1])
        except IndexError:
            return 1

    def scour(self, soup):
        results = soup.find_all("h3", \
            attrs={"class": "business-list-title"})
        titles = [h3.get_text().replace("&amp;", "&") for h3 in results]

        urls = []
        url_results = soup.find_all("div", \
            attrs={"class": "result-content"})
        for div in url_results:
            tags = div.find_all("a", href=True)
            for a in tags:
                url = str(a["href"])
                if url[0] != "h":
                    url = "https://www.sunbeltnetwork.com" + url
                urls.append(url)

       
        e_results = soup.find_all("p", attrs={"class": "excerpt"})
        excerpts = [p.get_text().replace("&amp;", "&") for p in e_results]

        details = []
        d_results = soup.find_all("div", attrs={"class": "result-details"})
        for div in d_results:
            tags = div.find_all("b")
            for tag in tags:
                details.append(tag.text)

        prices = details[::4]
        revenues = details[1::4]
        cashflows = details[2::4]
        locations = details[3::4]

        if self.positive_inputs is None and self.negative_inputs is None:
            scores = [Score(" ".join([x, y])) for x, y in zip(titles, excerpts)]
        else:
            scores = [Score(" ".join([x, y]), positive_inputs=self.positive_inputs, \
                negative_inputs=self.negative_inputs) for x, y in zip(titles, excerpts)]

        master_list = [titles, prices, revenues, cashflows, locations, \
            excerpts, scores, urls]
        
        return master_list

    def concat_pages(self, no_pages=-1):
        """Returns a full sorted DF across pages.
        If Kwarg no_pages = -1, we search all pages.
        Otherwise, Kwarg is the number of pages to search.
        """

        if no_pages == -1:
            last_page = self.count_pages()
        elif isinstance(no_pages, int):
            last_page = no_pages
        else:
            raise TypeError("No_pages must be an Integer.")
        
        master_list = self.scour(self.soup)
        for page in range(2, last_page + 1):
            current_scour = self.scour(self.soupify(occurance="next"))
            for entry in range(len(current_scour[0])):
                for idx, list_ in enumerate(master_list):
                    list_.append(current_scour[idx][entry])

        self.quit()
        return master_list

    def concat_states(self):
        """Combines the entries from different states. Returns a list 
        of each column in a sublist, across pages and states.
        """
        
        master_list = self.concat_pages()
        for state in self.other_states:
            current_scour = Sunbelt([state]).concat_pages()
            for entry in range(len(current_scour[0])):
                for idx, list_ in enumerate(master_list):
                    list_.append(current_scour[idx][entry])

        return master_list

    def make_dataframe(self):
        """Turns concatenated pages data into DF sorted by score."""

        master_list = self.concat_states()
        cols = ("Listing Title", "Price", "Revenue", "Cash Flow", \
            "Location", "Description", "Score", "URL")

        df = pd.DataFrame(dict(zip(cols, master_list)), columns=cols)
        df_sorted = df.sort_values(by=["Score"], ascending=False)
        return df_sorted

    def quit(self):
        self.driver.quit()
    


if __name__ == "__main__":
    state_inputs = input("Which states should we check? \n")
    inputs = [state.strip() for state in state_inputs.split(",")]
    start_time = time.time()
    case = Sunbelt(inputs)

    print("\nScraping Sunbelt.com...\n", end='')
    try:
        df_sorted = case.make_dataframe()
        print(df_sorted)
        print(f"\nCompleted in {time.time() - start_time}s.\n")
    except ValueError:
        print("Columns might be different sizes:")
        cols = ["Listing Title", "Price", "Revenue", "Cash Flow", \
            "Location", "Description", "Score", "URL"]
        for i, col in enumerate(cols):
            print(f"{col}: {len(case.scour()[i])}")
