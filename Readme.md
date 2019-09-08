## **Decisions made on scrubbing the dataframes** ##


***Physical activity measures and actions taken to fill in gaps in data:***

CANADA dataframe: In the Canadian csv file (CA_health_by_province.csv) there are 2 fields related to body activity in the “Indicators” field:

1.	Self-reported physical activity, 150 minutes per week, adult (18 years and over)
2.	Self-reported physical activity, average 60 minutes per day, youth (12 to 17 years old)

I decided to use the 150 minutes and 18 years and over because of the bigger pool of people and wider range of years. For consistency I chose the same parameter (150 minute per week) in the US csv file. There are not records related to body inactivity so I calculated the data by using the percent values. (% inactive people (unknown) = 100 - % active people (known)). I renamed the 1. record as “active” and the calculated record as “inactive”.

UNITED STATES dataframe: In the US health file (US_nutrition__physical_activity__and_obesity.csv) there are 3 records containing the string “150 minutes” in the “Question” field:

1.	Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity
2.	Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic
3.	Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic

I decided to use the first of the three and renamed the record as “active”. The first and second options were very similar. My choice was made purely on instinct given the lack of information I had on the database. For consistency with the Canadian dataframe I decided to calculate the “inactive” record using the percentage values (% inactive people (unknown) = 100 - % active people (known)).

***Body mass index measures and actions taken to fill in gaps in data:***

CANADA dataframe: In the Canadian csv file (CA_health_by_province.csv) there are 3 fields related to body mass index in the “Indicators” field:

1.	Body mass index, adjusted self-reported, adult (18 years and over), overweight
2.	Body mass index, adjusted self-reported, adult (18 years and over), obese
3.	Body mass index, self-reported, youth (12 to 17 years old), overweight or obese

I decided to use the first two options for 2 reasons. The first reason is the consistency with the activity data which were collected in a population aged 18 years and over. The second reason is the amount of information provided: 2 separated records for overweight and obese versus just one record with merged information. I renamed the option 1. as “overweight” and the option 2. as “obese”. There are not records related to normal body mass index so I calculated the data using the percent information. (% normal (unknown) =  100 - % obese (known) - % overweight (known)). I renamed the calculated records as “normal”.

United States dataframe: In the US health file (US_nutrition__physical_activity__and_obesity.csv) there are 2 records containing the strings "obesity" and "overweight" in the “Question” field:

1.	Percent of adults aged 18 years and older who have obesity
2.	Percent of adults aged 18 years and older who have an overweight classification

I decided to use both of the and rename the option 1. as “obese” and the option 2. as “overweight”. For consistency with the Canadian dataframe I calculated the “normal” record using the percent information. (% normal (unknown) =  100 - % obese (known) - % overweight (known)). I renamed the calculated data as “normal”.

***Household income :***

In US household file “US_household_income_by_zip.csv” I assumed that the information provided are the mean income per household. By checking the records in the Canadian census file (CA_full_census_by_FSA_code.csv) I decided to use the records “Average total income in 2015 among recipients ($)” which I assumed were comparable to the average household income in Canada dataframe.

***Files choice:***

US_40k_zips.csv contains the following meaningful fields: Zipcode, State abbreviation, Latitude, Longitude
US_household_income_by_zip.csv contains the following meaningful fields: Zipcode, State abbreviation, State Name, Latitude, Longitude and household income. Since the information in the first file are all included in the second one, I decided not to use it and to use only the second one.

***Merging decisions:***

I decided to merge df7 (US_population_by_zip_2010.csv) to df5 (US_household_income_by_zip.csv) on df5.zipcode. Although df7 has info on the zipcode it does have not info on the state of these zipcodes, longitude, latitude and household. So I decided to inner merge on the df5 zipcode so to have all the info about state, latitude, longitude and household
