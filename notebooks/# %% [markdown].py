# %% [markdown]
# # 1.0 Full Exploratory Data Analysis

# %% [markdown]
# ## Libraries

# %%
%load_ext autoreload
%autoreload 2

# %%
import sys
sys.path.append("..")
import final_project.utils.paths as path
import janitor
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %% [markdown]
# ## Download data

# %% [markdown]
# ### Specify input and output files

# %%
covid_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"

covid_file = path.data_raw_dir("time_series_covid19_confirmed_global.csv")

# %% [markdown]
# ### Run download

# %%
!curl {covid_url} -o {covid_file}

# %% [markdown]
# ## Process data

# %% [markdown]
# ### Read data

# %%
input_covid_file = path.data_raw_dir("time_series_covid19_confirmed_global.csv")

# %%
covid_df = pd.read_csv(input_covid_file)
covid_df.info()

# %%
covid_df.head()

# %% [markdown]
# ### Process data

# %%
processed_df = (
    covid_df
    .select_columns(["Country/Region", "*/*/*"])
    .pivot_longer(
        index="Country/Region",
        names_to="date"
    )
    .transform_column("date", pd.to_datetime)
    .clean_names()
)

processed_df.head()

# %% [markdown]
# ### Save output data

# %%
output_covid_file = path.data_processed_dir("time_series_covid19_confirmed_global_processed.csv")

# %%
processed_df.to_csv(output_covid_file, index=False)

# %% [markdown]
# ## Explore data

# %% [markdown]
# ### Read data

# %%
processed_covid_file = path.data_processed_dir("time_series_covid19_confirmed_global_processed.csv")

# %%
processed_covid_df = pd.read_csv(processed_covid_file)
processed_covid_df.info()

# %%
processed_covid_df.head()

# %% [markdown]
# ### Explore data

# %%
sns.set_style("whitegrid")

# %%
processed_covid_df = (
    processed_covid_df
    .transform_column(
        "date",
        pd.to_datetime
    )
)

# %% [markdown]
# #### Appearance of new covid-19 cases in Latam

# %% [markdown]
# Subset data.

# %%
countries = ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Mexico', 'Peru']
some_latam_countries_df = processed_covid_df.filter_on(f"country_region in {countries}")
some_latam_countries_df.head(3)

# %% [markdown]
# Plot time series.

# %%
import final_project.visualization.visualize as visualize

# %%
visualize.covid_time_series(some_latam_countries_df)

# %% [markdown]
# #### Latam in global context

# %% [markdown]
# Top `n` countries.

# %%
top_countries_df = (
    processed_covid_df
    .select_columns(["country_region", "value"])
    .groupby(["country_region"])
    .aggregate("sum")
    .sort_values("value", ascending=False)
    .reset_index()
    .head(20)
    .transform_column(
        column_name="country_region",
        function=lambda x: "red" if x in countries else "lightblue",
        dest_column_name="color"
    )
)

top_countries_df.head()

# %% [markdown]
# Plot to Latam in highlighted bars.

# %%
visualize.top_countries(top_countries_df)


