import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# A request to get raw HTML
webpage_response = requests.get("https://content.codecademy.com/courses/beautifulsoup/cacao/index.html")

# BeutifulSoup object to traverse webpage_response
soup = BeautifulSoup(webpage_response.content, "html.parser")

# Explore the HTML
print(soup)

# Get all tags that contain the ratings
rating = soup.find_all(attrs={"class":"Rating"})

# Create an empty list called ratings
ratings = []

# Loop through rating tags and append the the text contents of those tags to ratings
for text in rating:
  ratings.append(text.get_text())

# Remove the first element of ratings and assign the remaining data to a new ratings variable
ratings = ratings[1:]

# An empty list called ratings_to_float
ratings_to_float = []

# Loop through ratings data
for data in ratings:
  # Append a float type of each data point to ratings_to_float
  ratings_to_float.append(float(data))

# Create a histogram of the ratings_to_float values 
plt.hist(ratings_to_float)

# Show the plot
plt.show()

# Variable company_names to contain the tag with class Company
company_names = soup.select(".Company")

# Empty list called companies to hold the company names
companies = []

# Loop through company_names and add the text from each tag to companies
for tag in company_names[1:]:
  companies.append(tag.get_text())

# Create a dictionary d for companies and ratings_to_float data with keys "Company" and "Ratings"
d = {
  "Company": companies,
  "Ratings": ratings_to_float
}

# Create a DataFrame called df from d
cacao_df = pd.DataFrame.from_dict(d)

# Group cacao_df by "Company" and take the average of the grouped ratings
mean_ratings = cacao_df.groupby("Company").Ratings.mean()

# Get the 10 highest rated chocolate companies
ten_best = mean_ratings.nlargest(10)
print(ten_best)

# An empty list called cocoa_percents
cocoa_percents = []

# Access the tags with class "CocoaPercent
cocoa_percent_tags = soup.select(".CocoaPercent")

# Iterate through cocoa_percent_tags to get text content and data
for td in cocoa_percent_tags[1:]:
  percent = float(td.get_text().strip('%'))
  cocoa_percents.append(percent)

# Add cocoa_percents to the dictionary d with key "CocoaPercentage"
d["CocoaPercentage"] = cocoa_percents

# Create a DataFrame called df from updated d
cacao_df = pd.DataFrame.from_dict(d)

# A scatterplot of cacao_df.Ratings VS cacao_df.CocoaPercentage
plt.scatter(cacao_df.CocoaPercentage, cacao_df.Ratings)

# Get a line of best-fit
z = np.polyfit(cacao_df.CocoaPercentage, cacao_df.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(cacao_df.CocoaPercentage, line_function(cacao_df.CocoaPercentage), "r--")

# Show the plot
plt.show()

# Clear the figure between showing your histogram and this scatterplot
plt.clf()