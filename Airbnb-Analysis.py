
#Import Pandas for data analysis and matplotlib for data visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
from sklearn.linear_model import LinearRegression
import numpy as np

#Read csv file for NYC Airbnb data
df = pd.read_csv("nyc.csv")

#Drop any rows with null values
df.dropna(inplace=True)

#Drop any duplicate values present in data
df.drop_duplicates(inplace=True)

#Drop irrelevant columns
df = df.drop(['hostName', 'name', 'latitude', 'longitude', 'last_review', 'hostListings'], axis=1)

#Separate the data into 5 boroughs 
brooklyn = (df[df['Borough'] == 'Brooklyn'])
manhattan = (df[df['Borough'] == 'Manhattan'])
queens = (df[df['Borough'] == 'Queens'])
statenIsland = (df[df['Borough'] == 'Staten Island'])
bronx = (df[df['Borough'] == 'Bronx'])

#Calclate the average price per night for all 5 boroughs
avgBrooklyn = brooklyn['price'].agg('mean')
avgManhattan = manhattan['price'].agg('mean')
avgQueens = queens['price'].agg('mean')
avgStatenIsland = statenIsland['price'].agg('mean')
avgBronx = bronx['price'].agg('mean')

#Set up a for loop to determine which borough has the max mean price and the min mean price 
boroughs = {'Brooklyn': avgBrooklyn, 'Manhattan': avgManhattan, 'Queens': avgQueens, 'Staten Island': avgStatenIsland, 'Bronx': avgBronx}
minimum = None
maximum = None
minBorough = None
maxBorough = None
for borough, avgPrice in boroughs.items():
    if minimum is None or avgPrice < minimum:
        minimum = avgPrice
        minBorough = borough
    if maximum is None or avgPrice > maximum:
        maximum = avgPrice
        maxBorough = borough    

def getPriceLocation():
    #Use calculations from the for loop to print min mean price and max mean price per night
    outputmin = f"The borough with the lowest average price is {minBorough} with an average price of ${minimum:.2f}"
    outputmax = f"The borough with the highest average price is {maxBorough} with an average price of ${maximum:.2f}"
    print(outputmin)
    print(outputmax)
    
    #Create bar chart with each boroughs mean price per night
    types = ['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
    plot_data = [avgBrooklyn, avgManhattan, avgQueens, avgStatenIsland, avgBronx]
    bar_width = .45
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(types, plot_data, bar_width, color = 'blue')
    ax.set_xlabel('Borough')
    ax.set_ylabel('Average Price Per Night')
    ax.set_title('Average Price in Each Borough')
    fig.savefig('AvgPricePerBorough.png', bbox_inches = 'tight')
    
    
#Calculate the frequency of each borough in the dataset
boroughFreq = df['Borough'].value_counts(normalize=True)
  
def getBoroughFrequency():
    #Create a pie chart that shows the percentage of each borough
    plt.pie(boroughFreq.values, labels=boroughFreq.index, autopct='%1.1f%%')
    plt.title('Percentage of Each Borough in the Dataset')
    plt.savefig('BoroughFrequency.png', bbox_inches='tight')
    
    
#Concatenate the 'borough' and 'neighbourhood' columns to create a new column called 'area'
df['area'] = df['Borough'] + ', ' + df['neighbourhood']

#Calculate the mean price for each neighborhood in New York City - all 5 boroughs, Sort the neighborhoods by mean price then fetch the top 10
NYCPrices = df.groupby('area')['price'].mean().reset_index()
NYCPricesSorted = NYCPrices.sort_values('price', ascending=False)
top10NYCNeighborhoods = round(NYCPricesSorted.head(10), 2)

def getNYCNeighborhood():
    #Print the top 10 neighborhoods in New York City with the highest mean price
    print(top10NYCNeighborhoods)
        
    #Plot the output in a histogram
    plt.bar(top10NYCNeighborhoods['area'], top10NYCNeighborhoods['price'])
    plt.title('Top 10 Neighborhoods in NYC with the Highest Mean Price')
    plt.xlabel('Neighborhood, Borough')
    plt.ylabel('Mean Price')
    plt.xticks(rotation=90)
    plt.savefig('topNYCNeighborhoods.png', bbox_inches='tight')


#Calculate the mean price for each neighborhood in Manhattan, Sort the neighborhoods by mean price then fetch top 10
manhattanPrices = manhattan.groupby('neighbourhood')['price'].mean().reset_index()
manhattanPricesSorted = manhattanPrices.sort_values('price', ascending=False)
top10ManhattanNeighborhoods = round(manhattanPricesSorted.head(10), 2)

def getManhattanNeighborhood():
    #Print the top 10 neighborhoods in Manhattan with the highest mean price
    print(top10ManhattanNeighborhoods)
    
    #Plot the output in a histogram
    plt.bar(top10ManhattanNeighborhoods['neighbourhood'], top10ManhattanNeighborhoods['price'])
    plt.title('Top 10 Neighborhoods in Manhattan with the Highest Mean Price in Manhattan')
    plt.xlabel('Neighborhood')
    plt.ylabel('Mean Price')
    plt.xticks(rotation=90)
    plt.savefig('topManhattanNeighborhoods.png', bbox_inches='tight')


#Break down the three room types for units in Manhattan (private, home/apt, shared)
privateRoom = (manhattan[manhattan['roomType'] == ('Private room')])
aptRoom = (manhattan[manhattan['roomType'] == ('Entire home/apt')])
sharedRoom = (manhattan[manhattan['roomType'] == ('Shared room')])

#Calculate average price for the three differnt unit types
avgPrivRoom = privateRoom['price'].agg('mean')
avgAptRoom = aptRoom['price'].agg('mean')
avgSharedRoom = sharedRoom['price'].agg('mean')

#Calculate the frequency percent of each room type in Manhattan
percentPrivate = (privateRoom['price'].agg('count'))/(manhattan['price'].agg('count'))
percentApt = (aptRoom['price'].agg('count'))/(manhattan['price'].agg('count'))
percentShared = (sharedRoom['price'].agg('count'))/(manhattan['price'].agg('count'))

def getPriceRoom():
    #Print the average prices for the three different room types
    print(f"The average price for a private room in Manhattan is ${avgPrivRoom:.2f}")
    print(f"The average price for a home/apartment in Manhattan is ${avgAptRoom:.2f}")
    print(f"The average price for a shared room in Manhattan is ${avgSharedRoom:.2f}")
    
    #Plot the percent frequency of room type in pie chart
    plot_data = manhattan.groupby('roomType')['roomType'].count()
    total = plot_data.sum()
    plot_data = plot_data[plot_data > 0.01*total]
    pie = plt.figure()
    ax = pie.add_axes([0,0,1,1])
    ax.pie(plot_data.values, labels = ['Private Room', 'Home/Apt', 'Shared Room'], autopct='%1.1f%%')
    ax.set_title('Frequency of Room Type in Manhattan')
    pie.savefig('roomType.png', bbox_inches='tight')
   

#Break main dataframe into units that allow a one night stay and those who require more than 1 night at minimum
minimumNights = (df[df['minimumNights'] == 1])
moreThanOne = (df[df['minimumNights'] > 1])
    
#Break Manhattan dataframe into units that allow a one night stay and those who require more than 1 night at minimum
minimumNightsMan = (manhattan[manhattan['minimumNights'] == 1])
moreThanOneMan = (manhattan[manhattan['minimumNights'] > 1])

#Calculate the mean price per night for both 1 night min units and more than 1 night required
avgMinimumNights = minimumNights['price'].agg('mean')
avgMoreThanOne = moreThanOne['price'].agg('mean')

#Calculate the mean price per night for both 1 night min units and more than 1 night required in Manhattan
avgMinimumNightsMan = minimumNightsMan['price'].agg('mean')
avgMoreThanOneMan = moreThanOneMan['price'].agg('mean')

def getMinimum():
    #Print the output from above to show the average prices
    print(f"The average price for a unit in New York City that allow 1-night stays is ${avgMinimumNights:.2f}")
    print(f"The average price for a unit in New York City that requires more than 1 night minimum is ${avgMoreThanOne:.2f}\n")
    print(f"The average price for a unit in Manhattan that allow 1-night stays is ${avgMinimumNightsMan:.2f}")
    print(f"The average price for a unit in Manhattan that requires more than 1 night minimum is ${avgMoreThanOneMan:.2f}")
    
    #Make the variable minimum nights for df into binary data
    df['minimumNightsBinary'] = df['minimumNights'].apply(lambda x: 0 if x > 1 else 1)
    
    #Pie chart showing the distribution of 1 night min stays to all other minimum night stays
    plot_data = df.groupby('minimumNightsBinary')['minimumNightsBinary'].count()
    colors = ['purple', 'green']
    percentages = plot_data / plot_data.sum() * 100
    fig, ax = plt.subplots()
    ax.pie(percentages, labels=['1 Night Minimum', 'More than 1 Night Minimum'], autopct='%1.1f%%', colors=colors)
    ax.set_title('Percentage of listings with minimum nights')
    plt.savefig('minNight.png', bbox_inches = 'tight')
        
    
#Make new dataframe for units that have 150 or more nights of availability year round and less than 150 nights availability
moreAvailability = (df[df['availability'] >= 150])
lessAvailability = (df[df['availability'] < 150])

#Calculate the average price per night of units that have 150 or more nights of availability year round and less than 150 nights availability
avgMoreAvailability = moreAvailability['price'].agg('mean')
avgLessAvailability = lessAvailability['price'].agg('mean')

#Calculate average monthly reviews for units that have 150 or more nights of availability year round and less than 150 nights availability and standardize the amounts
monthlyReviewsMore = (moreAvailability['reviews_month'].agg('mean')/(150/365))
monthlyReviewsLess = lessAvailability['reviews_month'].agg('mean')

#Sample 1000 data points from each dataframe to make scatter plot that doesn't have too many observations
moreSample = moreAvailability.sample(n=1000, random_state=1)
lessSample = lessAvailability.sample(n=1000, random_state=1)

def getAvailability():
    #Print output from calculations above
    print(f"The average price for a unit with 150 or more nights of availability is ${avgMoreAvailability:.2f}")
    print(f"The average price for a unit with less than 150 nights of availability is ${avgLessAvailability:.2f}\n")
    print(f"The average monthly reviews for a unit with 150 or more nights of availability is {monthlyReviewsMore:.2f}")
    print(f"The average monthly reviews for a unit with less than 150 nights of availability is {monthlyReviewsLess:.2f}")
    
    #Create scatter plot from the randomly sampled datapoints above that has a max price per night of 500 to avoid outliers
    plt.scatter(moreSample['price'], moreSample['reviews_month'], color='red', alpha=0.5, label='150+ Days Availability')
    plt.scatter(lessSample['price'], lessSample['reviews_month'], color='blue', alpha=0.5, label='<150 Days Availability')
    plt.xlim([0,500])
    plt.ylim([0, 10])
    plt.xlabel('Price per Night')
    plt.ylabel('Reviews per Month')
    plt.legend()
    plt.savefig('reviewsXprices.png', bbox_inches = 'tight')

# Correlation Matrix
def plot_correlation_matrix():
    corr = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Correlation Matrix')
    plt.savefig('correlation_matrix.png', bbox_inches='tight')

# Distribution of Prices
def plot_price_distribution():
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'], bins=50, kde=True, color='blue')
    plt.title('Distribution of Prices')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.savefig('price_distribution.png', bbox_inches='tight')

# ANOVA Test between Boroughs
def perform_anova():
    brooklyn = df[df['Borough'] == 'Brooklyn']['price']
    manhattan = df[df['Borough'] == 'Manhattan']['price']
    queens = df[df['Borough'] == 'Queens']['price']
    staten_island = df[df['Borough'] == 'Staten Island']['price']
    bronx = df[df['Borough'] == 'Bronx']['price']

    f_stat, p_val = f_oneway(brooklyn, manhattan, queens, staten_island, bronx)
    print(f'ANOVA F-statistic: {f_stat:.2f}')
    print(f'ANOVA p-value: {p_val:.4f}')

# Box Plot for Price Distribution Across Boroughs
def plot_boxplot():
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Borough', y='price', data=df)
    plt.title('Price Distribution by Borough')
    plt.ylabel('Price')
    plt.xlabel('Borough')
    plt.savefig('boxplot_borough_prices.png', bbox_inches='tight')

# Linear Regression: Reviews vs. Price
def linear_regression_reviews_price():
    df['reviews_month'] = df['reviews_month'].replace('#DIV/0!', np.nan).astype(float)
    df.dropna(subset=['reviews_month'], inplace=True)

    X = df[['price']]
    y = df['reviews_month']

    model = LinearRegression()
    model.fit(X, y)

    plt.figure(figsize=(10, 6))
    plt.scatter(df['price'], df['reviews_month'], alpha=0.5, color='blue')
    plt.plot(df['price'], model.predict(X), color='red')
    plt.title('Linear Regression: Price vs. Reviews per Month')
    plt.xlabel('Price')
    plt.ylabel('Reviews per Month')
    plt.savefig('linear_regression_reviews_price.png', bbox_inches='tight')

# Call the functions to generate the plots and statistical analysis
plot_correlation_matrix()
plot_price_distribution()
perform_anova()
plot_boxplot()
linear_regression_reviews_price()