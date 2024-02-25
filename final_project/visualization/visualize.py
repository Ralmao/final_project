import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def top_countries(df:pd.DataFrame):
        sns.barplot(
            data=df,
            x="value",
            y="country_region",
            palette=df.color
        )

        plt.xlabel("Value")
        plt.ylabel("Country Region")
        plt.title("Latam countries in a global context");



def covid_time_series(df:pd.DataFrame):
        print("JAJAAJAJAJA")
        sns.lineplot(
        data=df,
        x="date",
        y="value",
        hue="country_region"
    )

        plt.xticks(rotation=15)
        plt.xlabel("Date")
        plt.ylabel("Value")
        plt.title("Latam covid time series");
