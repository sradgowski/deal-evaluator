from score import score as Score
import time
try:
    import bs4 as bs
    import pandas as pd
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    import install_requirements
    import bs4 as bs
    import pandas as pd
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

def soupify(url):
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" + \
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87" + \
            " Safari/537.36"}
    source = requests.get(url, headers=headers)
    soup = bs.BeautifulSoup(source.content, 'lxml')
    return soup

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
    
class TWorld():
    def __init__(self, states, mode="headless", positive_inputs=None, \
        negative_inputs=None):
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

        self.positive_inputs = positive_inputs
        self.negative_inputs = negative_inputs
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

    def __len__(self):
        return len(self.concat_states()[0])

    def __repr__(self):
        if self.state.lower() == "all":
            return "Transworld Listings for All U.S. States"
        else:
            states_here = ", ".join(self.other_states)
            full_states = ", ".join([states_here, self.state])
            return f"TWorld.com Listings for {full_states}"

    def __str__(self):
        states_here = ", ".join(self.other_states)
        full_states = ", ".join([states_here, self.state])
        return f"""TWorld.com Listings for States: {full_states}
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
            driver.get("https://www.tworld.com/buy-a-business/business-listing-search.php/")
            
            if self.state != "All":
                state = driver.find_element_by_id("state")
                state.send_keys(self.state)
            cf = driver.find_element_by_name("seller_price_min")
            cf.send_keys("700000")
            cf2 = driver.find_element_by_name("seller_price_max")

            # This will select 2,000,000, not 2,000
            cf2.send_keys("2,000")
            cf2.submit()
            time.sleep(1)

        elif occurance == "next":
            next_button = driver.find_element_by_partial_link_text("Next")
            next_button.click()
            time.sleep(1)
        else:
            raise ValueError("Occurance must be 'first' or 'next'.")

        soup = bs.BeautifulSoup(driver.page_source, "lxml")
        if " 0 businesses and companies for sale in" in str(soup):
            print("No businesses found.")
        return soup

    def count_pages(self, soup):
        try:
            results = soup.find_all("span", \
                attrs={"class": "page-link"})
            page_nos = [h3.get_text() for h3 in results]
            return int(page_nos[-1])
        except IndexError:
            return 1

    def scour(self, soup):
        """Pulls out information from a single page soup."""

        title_bin = soup.find("title").text
        title = title_bin[:title_bin.find(" |")]

        reason_bin = soup.find("input", attrs={"name": "reason"})
        category_bin = soup.find("input", attrs={"name": "category"})

        if reason_bin and category_bin:
            reason = reason_bin["value"]
            category = category_bin["value"]
            tagline = category + " firm, selling due to " + reason
        elif reason_bin:
            tagline = "Firm selling due to " + reason_bin["value"]
        elif category_bin:
            category = category_bin["value"]
            tagline = category + " firm, selling for undisclosed reason"
        else:
            tagline = "(No Tagline)"

        price_bin = soup.find("input", attrs={"name": "listing_price"})
        price = "$" + price_bin["value"]

        de_tag = "seller_discretionary_earnings"
        de_bin = soup.find("input", attrs={"name": de_tag})
        discretionary_earnings = "$" + de_bin["value"]

        loc_bin = soup.find("input", attrs={"name": "Location"})
        location = loc_bin["value"]
        if location[0] == ",":
            location = location[2:]

        tags = soup.find("meta", attrs={"name": "description"})
        description = tags["content"]

        contact_bin = soup.find("input", attrs={"name": "to_email"})
        contact = contact_bin["value"]

        if self.positive_inputs is None and self.negative_inputs is None:
            score = Score(" ".join([title, tagline, description]))
        else:
            score = Score(" ".join([title, tagline, description]), \
                positive_inputs=self.positive_inputs, \
                negative_inputs=self.negative_inputs)

        return [title, tagline, price, discretionary_earnings, \
            location, description, contact, score]

    def concat_pages(self):
        """Joines all of the results into a single master list."""
        master_list = [[] for i in range(9)]
        home = self.soupify()
        
        result = "result-item position-relative"

        mydivs = home.find_all("div", attrs={"class": result})
        atags = [div.a["href"] for div in mydivs]
        urls = ["http://www.tworld.com/" + a for a in atags]

        for i in range(self.count_pages(home) - 1):
            page = self.soupify(occurance="next")
            mydivs = page.find_all("div", attrs={"class": result})
            atags = [div.a["href"] for div in mydivs]
            hrefs = ["http://www.tworld.com/" + a for a in atags]
            urls.extend(hrefs)

        # Visit each url and log the soup
        for url in urls:
            try:
                soup =  soupify(url)
                results = self.scour(soup)
                master_list[8].append(url)
                for i, entry in enumerate(results):
                    master_list[i].append(entry)
            except TypeError:
                pass

        return master_list

    def concat_states(self):
        """Combines the entries from different states. Returns a list 
        of each column in a sublist, across pages and states.
        """
        
        master_list = self.concat_pages()
        for state in self.other_states:
            current_scour = TWorld([state]).concat_pages()
            for entry in range(len(current_scour[0])):
                for idx, list_ in enumerate(master_list):
                    list_.append(current_scour[idx][entry])

        return master_list

    def make_dataframe(self):
        """Turns concatenated pages data into DF sorted by score."""

        master_list = self.concat_states()
        cols = ("Listing Title", "Tagline", "Price", \
            "Discretionary Earnings", "Location", "Description", \
            "Contact Email", "Score", "URL")

        df = pd.DataFrame(dict(zip(cols, master_list)), columns=cols)
        df_sorted = df.sort_values(by=["Score"], ascending=False)
        self.quit()
        
        return df_sorted

    def quit(self):
        self.driver.quit()


if __name__ == "__main__":
    state_inputs = input("Which states should we check? \n")
    inputs = [state.strip() for state in state_inputs.split(",")]
    start_time = time.time()
    case = TWorld(inputs, mode="show")
    print("\nScraping TWorld.com...\n", end='')
    
    try:
        df_sorted = case.make_dataframe()
        print(df_sorted)
        print(f"\nCompleted in {time.time() - start_time}s.\n")
    except ValueError:
        print("Columns might be different sizes:")
        cols = ("Listing Title", "Tagline", "Price", \
            "Discretionary Earnings", "Location", "Description", \
            "Contact Email", "Score", "URL")
        for i, col in enumerate(cols):
            print(f"{col}: {len(case.scour()[i])}")
