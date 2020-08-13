from score import score as Score
import time
try:
    import bs4 as bs
    import pandas as pd
    import requests
except ImportError:
    import install_requirements
    import bs4 as bs
    import pandas as pd
    import requests

def soupify(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 \
        Safari/537.36'}
    source = requests.get(url, headers=headers)
    soup = bs.BeautifulSoup(source.content, 'lxml')
    return soup


class MergerTech():
    def __init__(self, positive_inputs=None, negative_inputs=None):
        self.url = "https://mergertech.com/current-engagements/"
        self.soup = soupify(self.url)
        self.positive_inputs = positive_inputs
        self.negative_inputs = negative_inputs

    def __len__(self):
        return len(self.scour()[0])

    def __repr__(self):
        return """Listings on MergerTech.com of all companies currently \
            engaged in sell-side advisor services"""

    def __str__(self):
        return """Listings on MergerTech.com of all companies currently \
            engaged in sell-side advisor services"""

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

    def scrape_titles(self):
        titles = [h4.get_text() for h4 in self.soup.findAll("h4")]
        return [title[8:] for title in titles]

    def scrape_tags_and_descriptions(self):
        ptags = self.soup.findAll("p")

        # First <p> is page description, last two are email/phone
        # Every 3rd <p> is "Click here..."
        tagl = [p.get_text().replace("&amp;","&") for p in ptags[1:-2:3]]
        desc = [p.get_text().replace("&amp;","&") for p in ptags[2:-1:3]]
        return [tagl, desc]

    def scrape_email_info(self):
        atags = self.soup.findAll("a", attrs={"class": "icon-email"})
        return [str(a.get("href")) for a in atags]

    def scour(self):
        """Returns a full list of results, categorized in sublists."""

        master_list = [self.scrape_titles(),  \
            self.scrape_tags_and_descriptions()[0], \
            self.scrape_tags_and_descriptions()[1], [], \
            self.scrape_email_info()]
        
        if self.positive_inputs is None and self.negative_inputs is None:
            for i, desc in enumerate(master_list[2]):
                master_list[3].append(Score(" ".join([master_list[0][i], \
                    master_list[1][i], desc])))
        else:
            for i, desc in enumerate(master_list[2]):
                master_list[3].append(Score(" ".join([master_list[0][i], \
                    master_list[1][i], desc]), \
                    positive_inputs=self.positive_inputs, \
                    negative_inputs=self.negative_inputs))

        return master_list

    def make_dataframe(self):
        """Turns concatenated pages data into DF sorted by score."""

        master_list = self.scour()
        cols = ("Listing Title", "Tagline", "Description", "Score", \
            "Contact Email")

        df = pd.DataFrame(dict(zip(cols, master_list)), columns=cols)
        df_sorted = df.sort_values(by=["Score"], ascending=False)
        return df_sorted


if __name__ == "__main__":
    start_time = time.time()
    case = MergerTech()

    print("\nScraping MergerTech.com...\n", end='')
    try:
        df_sorted = case.make_dataframe()
        print(case)
        print(df_sorted)
        print(f"\nCompleted in {time.time() - start_time}s.\n")
    except ValueError:
        print("Columns might be different sizes:")
        cols = ("Listing Title", "Tagline", "Description", \
            "Score", "Contact Email")
        for i, col in enumerate(cols):
            print(f"{col}: {len(case.scour()[i])}")
    
