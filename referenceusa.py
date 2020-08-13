try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    import bs4 as bs
    import pandas as pd
    from score import score as Score
except ImportError:
    import install_requirements
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    import bs4 as bs
    import pandas as pd
    from score import score as Score

states_list = ("Alabama", "Alaska", "Arizona", "Arkansas", "California", \
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", \
    "Idaho","Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", \
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", \
    "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", \
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", \
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", \
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", \
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", \
    "West Virginia", "Wisconsin", "Wyoming", "District of Colombia", \
    "Puerto Rico", "Virgin Islands", "Guam", "Marshall Islands", \
    "Micronesia", "Palau", "Northern Marianas", "All")
    
root = "http://www.referenceusa.com/UsBusiness/"
main_url = root + "Search/Custom/4e4e45b3474f4761a3e2180d05cb314f"

class ReferenceUSA():
    def __init__(self, states, mode="headless"):
        """Mode is either "headless" for no window popping up,
        or "show" if you want to watch the browser run.
        """

        if not isinstance(states, list):
            raise TypeError("States must be in a list.")

        self.states = states
        if not isinstance(self.states, list):
            raise TypeError("States must be in a list.")
        for state in self.states:
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

    def __len__(self):
        return len(self.scour()[0])

    def __repr__(self):
        if self.states[0].lower() == "all":
            return "SunbeltNetwork.com Listings for All U.S. States"
        else:
            states_here = ", ".join(self.states)
            return f"ReferenceUSA.com Listings for {states_here}"

    def __str__(self):
        states_here = ", ".join(self.other_states)
        full_states = ", ".join([states_here, self.state])
        return f"""ReferenceUSA.com Listings for States: {full_states}
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
        """Opens the webpage and finds search results.
        You must already be on a VPN with access to the database,
        like the Yale Cisco Anyconnect VPN. The large chunk of code
        is entering in all of our preferences, alotting for loading
        time in between widgets being selected and appearing.
        """

        driver = self.driver
        if occurance == "first":
            driver.get(main_url)
            clear = driver.find_element_by_xpath\
            ("//a[@class='standardButtons grayMedium action-clear-search']")
            clear.click()

            wait = WebDriverWait(driver, 10)
            wait.until(EC.visibility_of_element_located((By.ID, \
                "cs-MajorIndustryGroup")))

            elements = ["cs-MajorIndustryGroup", "cs-EmployeeSize", \
                "cs-SalesVolume", "cs-HoldingStatus", "cs-ForeignParent", \
                "cs-HomeBasedBusiness", "cs-CityState"]
            for element_id in elements:
                component = driver.find_element_by_id(element_id)
                component.click()
            
            wait.until(EC.visibility_of_element_located((By.XPATH, \
                "//input[@value='70-89']")))
            time.sleep(2)
            business_vals = ["70-89", "99-99"]
            for val in business_vals:
                pick = driver.find_element_by_xpath(f"//input[@value='{val}']")
                pick.click()

            wait.until(EC.visibility_of_element_located((By.XPATH, \
                "//span[@class='label'][text()='50-99']")))
            wait.until(EC.visibility_of_element_located((By.XPATH, \
                "//span[@class='label'][text()='$20-50 Million']")))
            employee_vals = ["1-4", "5-9", "10-19", "20-49", "50-99"]
            sales_vals = ["$2.5-5 Million", "$5-10 Million", \
                "$10-20 Million", "$20-50 Million"]
            for val in employee_vals + sales_vals:
                span = driver.find_element_by_xpath\
                    (f"//span[@class='label'][text()='{val}']")
                span.click()

            wait.until(EC.visibility_of_element_located((By.XPATH, \
                "//label[@class='checkbox'][@for='Public']")))
            inclusion_settings = {"Public": "checkbox", "ExcludeHomeBased": \
                "radio tiny", "ExcludeForeignParent": "radio tiny"}
            for key, val in inclusion_settings.items():
                label = driver.find_element_by_xpath\
                    (f"//label[@class='{val}'][@for='{key}']")
                label.click()

            wait.until(EC.visibility_of_element_located((By.XPATH, \
                "//span[@class='label'][text()='California']")))
            if self.states[0] != "All":
                for state in self.states:
                    label = driver.find_element_by_xpath\
                        (f"//span[@class='label'][text()='{state}']")
                    label.click()

            search = driver.find_element_by_xpath\
            ("//a[@class='standardButtons greenMedium action-view-results']")
            search.click()
            time.sleep(3) 

            wait3 = WebDriverWait(self.driver, 10)
            wait3.until(EC.visibility_of_element_located((By.XPATH, \
                "//a[@class='action-view-record']")))

        elif occurance == "next":
            next_button = driver.find_element_by_class_name("next")
            next_button.click()
            time.sleep(1)
        else:
            raise ValueError("Occurance must be 'first' or 'next'.")

        soup = bs.BeautifulSoup(driver.page_source, "lxml")
        return soup

    def scrape(self, soup):
        """Pulls out information from a single soup."""

        title = soup.find("span", attrs={"class": \
            "data-record-title"}).get_text()
        location = soup.find("span", attrs={"class": \
            "data-record-subtitle secondary"}).get_text()
        tags = [tag.get_text() for tag in soup.find_all("td", \
            attrs={"class": "primary strong"})]
        industry = ", ".join(tags)

        # Plenty of divs, first 'p' is job listings.
        cutlines = []
        table = soup.find_all("div", attrs={"class": "groupboxContent"})
        for x in table:
            try:
                cutlines.append(x.find('p').text)
            except AttributeError:
                pass

        try:
            description = cutlines[1]
        except IndexError:
            description = cutlines[0]

        score = Score(" ".join([description, title, industry]))

        return [title, location, industry, description, score]

    def concat_listings(self):
        """Goes through all of the listings on a results page."""
        master_list = [[] for i in range(6)]
        home = self.soupify()
        
        atags = home.find_all("a", attrs={"class": "action-view-record"})
        urls = ["http://www.referenceusa.com" + a["data-all-url"].replace\
            ("All", "Tagged") for a in atags]
        
        i = 2
        while True:
            try:
                print(f"Round {i}...")
                next_page = self.soupify(occurance="next")
                atags = home.find_all("a", attrs={"class": "action-view-record"})
                new_urls = ["http://www.referenceusa.com" + a["data-all-url"].replace\
                    ("All", "Tagged") for a in atags]
                urls.extend(new_urls)
                i += 1
            except:
                break

        # Visit each url and log the soup
        wait = WebDriverWait(self.driver, 10)
        for url in urls:
            master_list[5].append(url)
            self.driver.get(url)
            time.sleep(1.5)
            soup =  bs.BeautifulSoup(self.driver.page_source, "lxml")
            results = self.scrape(soup)
            for i, entry in enumerate(results):
                master_list[i].append(entry)

        return master_list

    def make_dataframe(self):
        """Turns concatenated pages data into DF sorted by score."""

        master_list = self.concat_listings()
        cols = ("Listing Title", "Location", "Industry", "Description", \
            "Score", "URL")

        df = pd.DataFrame(dict(zip(cols, master_list)), columns=cols)
        return df.sort_values(by=["Score"], ascending=False)

    def to_excel(self):
        df = self.make_dataframe()
        return df.to_excel("referenceusaresults.xlsx")

    def quit(self):
        self.driver.quit()
    

if __name__ == "__main__":
    state_inputs = input("Which states should we check? \n")
    inputs = [state.strip() for state in state_inputs.split(",")]
    start_time = time.time()
    print("\nScraping ReferenceUSA.com...\n", end='')

    case = ReferenceUSA(inputs, mode='show')
    try:
        df_sorted = case.make_dataframe()
        print(df_sorted)
        print(f"\nCompleted in {time.time() - start_time}s.\n")
    except ValueError:
        print("Columns might be different sizes:")
        cols = ("Listing Title", "Location", "Industry", \
            "Description", "URL")
        for i, col in enumerate(cols):
            print(f"{col}: {len(case.scour()[i])}")
    
