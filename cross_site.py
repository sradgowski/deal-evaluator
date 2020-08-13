import bizbuysell as bbs
import mergertech as mt
import os
import pandas as pd
import sqlite3
import sunbelt as sb
import sys
import time
import tworld as tw

pd.options.mode.chained_assignment = None
cols = ("Listing Title", "Tagline", "Cash Flow", "Description", \
    "Score", "URL", "Source")


class FullScrape():
    def __init__(self, include=["bbs", "mt", "sb", "tw"], positive_inputs=None, \
        negative_inputs=None):
        self.inclusions = include

        if positive_inputs is None and negative_inputs is None:
            self.bbs_frame = bbs.BizBuySell(["All"]).make_dataframe()
            self.mt_frame = mt.MergerTech().make_dataframe()
            self.sb_frame = sb.Sunbelt(["All"]).make_dataframe()
            self.tw_frame = tw.TWorld(["All"]).make_dataframe()
        else:
            self.bbs_frame = bbs.BizBuySell(["All"], positive_inputs=positive_inputs, \
                negative_inputs=negative_inputs).make_dataframe()
            self.mt_frame = mt.MergerTech(positive_inputs=positive_inputs, \
                negative_inputs=negative_inputs).make_dataframe()
            self.sb_frame = sb.Sunbelt(["All"], positive_inputs=positive_inputs, \
                negative_inputs=negative_inputs).make_dataframe()
            self.tw_frame = tw.TWorld(["All"], positive_inputs=positive_inputs, \
                negative_inputs=negative_inputs).make_dataframe()

    def concat_frames(self):
        frames = []
        if "bbs" in self.inclusions:
            bbs_edit = self.bbs_frame
            bbs_edit.insert(6, "Source", "BizBuySell.com")
            frames.append(bbs_edit)
        
        if "mt" in self.inclusions:
            mt_edit = self.mt_frame
            mt_edit.rename(columns={"Contact Email": "URL"}, \
                inplace=True)
            mt_edit.insert(2, "Cash Flow", "(No Cash Flow listed)")
            mt_edit.insert(6, "Source", "MergerTech.com")
            frames.append(mt_edit)

        if "sb" in self.inclusions:
            sb_edit = self.sb_frame[["Listing Title", "Cash Flow", \
                "Description", "Score", "URL"]]
            sb_edit.insert(1, "Tagline", "(No Tagline)")
            sb_edit.insert(6, "Source", "SunbeltNetwork.com")
            frames.append(sb_edit)

        if "tw" in self.inclusions:
            tw_edit = self.tw_frame[["Listing Title", "Tagline", \
                "Discretionary Earnings", "Description", "Score", "URL"]]
            tw_edit.rename(columns={"Discretionary Earnings": "Cash Flow"}, \
                inplace=True)
            tw_edit.insert(6, "Source", "TWorld.com")
            frames.append(tw_edit)

        df = pd.concat(frames)
        df_sorted = df.sort_values(by=["Score"], ascending=False)
        return df_sorted

    def find_new(self, df):
        """Returns a new DataFrame with only the entries
        from the paramater df passed in that are not
        already in the past_scrapes SQL Database.
        """

        path = os.path.dirname(sys.modules[__name__].__file__)
        connection = sqlite3.connect("appbin/past_scrapes.db")
        c = connection.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS
            scrape_history(
            listing_title text,
            tagline text,
            cash_flow text,
            description text,
            score integer,
            url text,
            source text,
            scrape_date date)""")

        new_rows = []
        for index, row in df.iterrows():
            title = str(row["Listing Title"])
            url = str(row["URL"])
            c.execute("""SELECT * FROM scrape_history 
            WHERE listing_title=?
            AND url=?""", (title, url))
            exists = c.fetchall()
            if not exists:
                new_rows.append(row.values)

        connection.commit()
        connection.close()
        return pd.DataFrame(new_rows, columns=cols)

    def add_to_db(self, df):
        connection = sqlite3.connect("appbin/past_scrapes.db")
        c = connection.cursor()
        command = """INSERT INTO 
            scrape_history(listing_title, tagline, cash_flow,
            description, score, url, source, scrape_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, date('now'))
            """

        for index, row in df.iterrows():
            package = (row["Listing Title"], row["Tagline"], \
                row["Cash Flow"], row["Description"], row["Score"], \
                row["URL"], row["Source"])
            c.execute(command, package)
        
        connection.commit()
        connection.close()

    def check_above_score(self, min_score, setting):
        """Setting is either 'new' for new listings at or 
        above the minimum score, or 'all' for all listings at
        or above the minimum score.
        Returns a tuple of the new df and the number of total
        new listings.
        """

        df = self.concat_frames()
        new_df = self.find_new(df)
        new_above_min = new_df[new_df.Score >= min_score]
        self.add_to_db(new_df)
       
        if setting == "new":
            return (new_above_min, len(new_df))
        elif setting == "all":
            return (df[df.Score >= min_score], len(new_df))
        else:
            raise ValueError("Setting should be 'new' or 'all'.")


if __name__ == "__main__":
    start_time = time.time()
    case = FullScrape()
    new = case.check_above_score(2, "new")
    print(f"Length of new df: {new[1]}\n")

    print(new[0])
    print(f"\nCompleted in {time.time() - start_time}s.\n")
