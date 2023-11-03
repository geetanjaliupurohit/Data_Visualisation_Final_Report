import pandas as pd
import re

# Read category names
category_names = pd.read_pickle("category_names.pkl")  # Assuming you have a pickled file

# Define column names
col_nm = [
    "category", "total_estimate", "total_moe3", "men_estimate", "men_moe3",
    "women_estimate", "women_moe3", "percent_women", "percent_women_moe3",
    "total_earnings_estimate", "total_earnings_moe3", "total_earnings_men_estimate",
    "total_earnings_men_moe3", "total_earnings_women_estimate", "total_earnings_women_moe3",
    "wage_percent_of_mens_estimate", "wage_percent_of_mens_moe3"
]

# Read and clean data for each year
def read_and_clean_data(year, filename, skip_rows, category_names):
    df = pd.read_excel(filename, skiprows=skip_rows)
    df.columns = col_nm
    df = df.dropna(subset=['total_estimate'])
    df['year'] = year
    df['category'] = category_names
    return df

# initial 6 rows don't contain data according format from US beaura site
earnings_2013 = read_and_clean_data(2013, "median-earnings-2013-final.xlsx", 6, category_names)
earnings_2014 = read_and_clean_data(2014, "median-earnings-2014-final.xlsx", 6, category_names)
earnings_2015 = read_and_clean_data(2015, "median-earnings-2015-final.xlsx", 6, category_names)
earnings_2016 = read_and_clean_data(2016, "median-earnings-2016-final.xlsx", 6, category_names)
earnings_2014 = read_and_clean_data(2017, "median-earnings-2017-final.xlsx", 6, category_names)
earnings_2015 = read_and_clean_data(2018, "median-earnings-2018-final.xlsx", 6, category_names)
earnings_2016 = read_and_clean_data(2019, "median-earnings-2019-final.xlsx", 6, category_names)
earnings_2014 = read_and_clean_data(2020, "median-earnings-2020-final.xlsx", 6, category_names)
earnings_2015 = read_and_clean_data(2021, "median-earnings-2021-final.xlsx", 6, category_names)


# Concatenate data for all years
all_years = pd.concat([earnings_2013, earnings_2014, earnings_2015, earnings_2016])

# Define category lists
cat1 = [
    "Management, Business, and Financial Occupations",
    "Computer, Engineering, and Science Occupations",
    "Education, Legal, Community Service, Arts, and Media Occupations",
    "Healthcare Practitioners and Technical Occupations",
    "Service Occupations",
    "Sales and Office Occupations",
    "Natural Resources, Construction, and Maintenance Occupations",
    "Production, Transportation, and Material Moving Occupations"
]

cat2 = [
    "Management Occupations",
    "Business and Financial Operations Occupations",
    "Computer and mathematical occupations",
    "Architecture and Engineering Occupations",
    "Life, Physical, and Social Science Occupations",
    "Community and Social Service Occupations",
    "Legal Occupations",
    "Education, Training, and Library Occupations",
    "Arts, Design, Entertainment, Sports, and Media Occupations",
    "Healthcare Practitioners and Technical Occupations",
    "Healthcare Support Occupations",
    "Protective Service Occupations",
    "Food Preparation and Serving Related Occupations",
    "Building and Grounds Cleaning and Maintenance Occupations",
    "Personal Care and Service Occupations",
    "Sales and Related Occupations",
    "Office and Administrative Support Occupations",
    "Farming, Fishing, and Forestry Occupations",
    "Construction and Extraction Occupations",
    "Installation, Maintenance, and Repair Occupations",
    "Production Occupations",
    "Transportation Occupations",
    "Material Moving Occupations"
]

# Add category columns
all_years['cat1'] = all_years['category'].apply(lambda x: x if x in cat1 else None)
all_years['cat2'] = all_years['category'].apply(lambda x: x if x in cat2 else None)

# Clean category names
all_years['cat1'] = all_years['cat1'].str.replace(" Occupations", "").str.replace(" occupations", "")
all_years['cat2'] = all_years['cat2'].str.replace(" Occupations", "").str.replace(" occupations", "")
all_years['category'] = all_years['category'].str.replace(" Occupations", "").str.replace("occupations", "")

# Fill missing values in category columns
all_years['cat1'] = all_years['cat1'].fillna(method='ffill')
all_years['cat2'] = all_years['cat2'].fillna(method='ffill')

# Define final column names
nm_final = [
    "year", "occupation", "major_category", "minor_category", "total_employees",
    "no_male_employees", "no_female_employees", "female_percentage", "total_pay",
    "male_total_pay", "total_earnings_female", "pay_percent_of_male"
]

# Filter and select columns
final_all = all_years[~all_years['category'].str.contains('|'.join(cat1 + cat2)) &
                     (all_years['cat1'].notna()) &
                     (all_years['cat2'].notna())]
final_all = final_all.rename(columns={'category': 'occupation', 'cat1': 'major_category', 'cat2': 'minor_category'})
final_all = final_all[nm_final]

# Convert numeric columns to numeric
final_all[['total_earnings', 'total_earnings_male', 'total_earnings_female', 'wage_percent_of_male']] = \
    final_all[['total_earnings', 'total_earnings_male', 'total_earnings_female', 'wage_percent_of_male']].apply(pd.to_numeric)

# Print the resulting DataFrame
print(final_all)