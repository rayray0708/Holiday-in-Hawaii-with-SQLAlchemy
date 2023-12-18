![Illustration of Honolulu, Hawaii](https://gumlet.assettype.com/outlooktraveller%2Fimport%2Foutlooktraveller%2Fpublic%2Fuploads%2Farticles%2Fexplore%2FUntitled_design_-_2023-07-14T183536_209.jpg?auto=format%2Ccompress&fit=max&format=webp&w=768&dpr=2.0)
# Holiday-in-Hawaii-with-SQLAlchemy
## Description
In this project, I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii. In order to plan the trip, I've decided to do a climate analysis about the area. There're 2 parts to this project. In Part 1 of the project, I use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, I have used SQLAlchemy ORM queries, Pandas, and Matplotlib. In part 2 of the project, I designed a Flask API based on the queries that I have just developed in Part 1. 

## Usage
To see the code for Part 1, navigate to the SurfsUp folder and open climate_starter.ipynb.

To see the code for Part 2, navigate to the SurfsUp folder and open app.py.

*note: in order to make my JSON output more descriptive, I've added 'station' as the key and the station's name as the value for each key:value pair for question 3 of Part 2. I've done the same for question 4 (adding the date key:value pair and temperature key:value pair to make the json output more descriptive).

## Installation
The following dependencies have been installed for this project. Please copy the code to your code editor as is:
1) Matplotlib\
`%matplotlib inline`\
`from matplotlib import style`\
`style.use('fivethirtyeight')`\
`import matplotlib.pyplot as plt`
2) `import numpy as np`
3) `import pandas as pd`
4) `import datetime as dt`
5) SQLAlchemy\
`import sqlalchemy`\
`from sqlalchemy.ext.automap import automap_base`\
`from sqlalchemy.orm import Session`\
`from sqlalchemy import create_engine, func`\
`from sqlalchemy import desc`

Please make sure you have the following libraries pre-installed:
1. `!pip install pandas`
2. `!pip install sqlalchemy`
3. `!pip install matplotlib`
4. `!pip install numpy`

## Climate analysis using SQLAlchemy
Our dataset contains the following columns:
![Alt text](<Screenshot 2023-12-18 at 1.48.26 pm.png>)

Starting from the most recent data point in the database, I retrieved the last 12 months of precipitation data and plotted the results. After that, I saved the query results as a Pandas DataFrame and explicitly set the column names. Finally, I sorted the dataframe by date.

The plot contains the following information:
1. `x='date'`, `y='precipitation'`, `rot = 90`
2. `plt.xlabel('Date')`
3. `plt.ylabel('Precipitation (mm)')`
4. `plt.title('Precipitation by month')`

![Alt text](<Screenshot 2023-12-18 at 2.02.28 pm.png>)

Additionally, I plotted the temperatures in the last 12 months, starting from 23/08/2017. 
![Alt text](<Screenshot 2023-12-18 at 2.05.01 pm.png>)

## Credits
Special thanks to the following individuals for their contribution:

-Reza Abasaltian (BCS tutor)

-AskBCS learning assistants
