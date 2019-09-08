
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#loading files
df1 = pd.read_csv('CA_full_census_by_FSA_code.csv')
df2 = pd.read_csv('CA_age_by_FSA_code.csv')
df3 = pd.read_csv('CA_health_by_province.csv')
df4 = pd.read_csv('US_40k_zips.csv')
df5 = pd.read_csv('US_household_income_by_zip.csv')
df6 = pd.read_csv('US_nutrition__physical_activity__and_obesity.csv')
df7 = pd.read_csv('US_population_by_zip_2010.csv')

#Creates a dictionary to associate a Canadian region to its postal code
dictionary = {'Alberta' : 'T',
              'British Columbia' : 'V',
              'Manitoba' : 'R',
              'New Brunswick' : 'E',
              'Newfoundland and Labrador' : 'A',
              'Nova Scotia' : 'B',
              'Nunavut' : 'X',
              'Northwest Territories': 'X',
              'Ontario' : 'L,N,K,M,P',
              'Quebec' : 'G,H,J',
              'Saskatchewan' : 'S',
              'Yukon' : 'Y',
              'Prince Edward Island' : 'C'}


################## Preparation of the Canada Dataframe: df_CA ##################
#############
########
###


# -----------------df1 (CA_full_census_by_FSA_code.csv)-----------------

df1 = df1.rename(columns={'GEO_NAME' : "region_ab",'DIM: Profile of Forward Sortation Areas (2247)' : 'profile', 'Dim: Sex (3): Member ID: [2]: Male' : 'male_household','Dim: Sex (3): Member ID: [3]: Female' : 'female_household', 'Dim: Sex (3): Member ID: [1]: Total - Sex' : 'total'})
df1 = df1[['region_ab', 'profile', 'male_household', 'female_household']] #reduces the database to only 6 fields
df1 = df1[~df1.region_ab.str.contains("Canada")] #drops all the rows containing , and Canada in the 'GEO' field
df1 = df1[df1['profile'].str.contains('Average total income in 2015 among recipients')] #keeps all the rows containing Number and Percent in the 'Characteristics' field
df1 = df1[pd.to_numeric(df1['male_household'], errors='coerce').notnull()] #drops all the rows not having numeric data in the 'total' field
df1 = df1.replace (['X0A','X0B','X0C'], 8) #Nunavut region shares same first letter of the postal code with Northwest Territories. So before
                                           #trimming the string to the first letter (X) and losing info on the region, I renamed these region with an integer
df1['zip/FSA'] = df1['region_ab'].astype(str).str[0] #it keeps only the first letter of each string. Nunavut having an integer (8) in the zip/FSA field is not affected
df1 = df1.drop(['region_ab', 'profile'], axis=1)

df1 = df1.replace (['K','L','N','M','P'], 'L,N,K,M,P') #renames the postcode of Ontatio region to group them in 1 unique string
df1 = df1.replace (['G','H','J'], 'G,H,J') #renames the postcodes of Quebec region to group all of them in 1 unique string
df1 = df1 [['zip/FSA','male_household','female_household']] #Reorders the columns in df3
df1[['male_household','female_household']] = df1[['male_household','female_household']].astype(float) #Changes to float tht dtype of the fields
df1 = df1.groupby(['zip/FSA']).mean()
df1 = df1.reset_index()


inv_dictionary = {v: k for k, v in dictionary.items()} #inverts the dictionary
df1['state/region'] = df1['zip/FSA'].map(inv_dictionary) #use inverted dictionary to associate zip/FSA to state/region
df1.iloc[0,0] = 'X'
df1.iloc[0,3] = 'Nunavut'

# creating 2 dataframe to join male population and female population in the same column (from the original 2 columns)
df1_male = df1[['zip/FSA','male_household','state/region']]
df1_male = df1_male.rename(columns={'male_household' : 'household'})
df1_male['gender'] = 'male'

df1_female = df1[['zip/FSA','female_household','state/region']]
df1_female = df1_female.rename(columns={'female_household' : 'household'})
df1_female['gender'] = 'female'

df1 = pd.concat([df1_male, df1_female], keys=['x', 'y'], sort=False) #concatenating the 2 dataframe



# -----------------df3 (CA_health_by_province.csv)-----------------

df3 = df3[['GEO','Age group', 'Sex', 'Indicators', 'Characteristics', 'VALUE']] #reduces the database to only 6 fields
df3 = df3[~df3.GEO.str.contains(",|Canada")] #drops all the rows containing , and Canada in the 'GEO' field
df3 = df3[df3['Characteristics'].str.contains('Number |Percent')] #keeps all the rows containing Number and Percent in the 'Characteristics' field
df3 = df3[df3['Age group']=='Total, 12 years and over'] #it filters only for the rows having 'Total, 12...' in the 'Age group' field

df3 = df3[df3['Indicators'].str.contains("Body mass index, adjusted | 150 minute|Diabetes|Mood")] #keeps all the rows containing 'Body mass, adjusted' and '150 minute' in the 'Indicators' field
df3 = df3.rename(columns={'VALUE' : "population",'GEO' : 'state/region','Sex' : 'gender', 'Age group' : 'age'})
df3['country'] = 'Canada' #adds a column 'Country' with Canada values in it
df3 = df3[~df3.gender.str.contains("Both")] #drops all the rows containing 'Both' in the 'Gender' field

df3['zip/FSA'] = df3['state/region'].map(dictionary) #merges the dictionary values with df3 on 'State/Region' field and creates a new field 'zip/FSA'
df3 = df3 [['zip/FSA','country','state/region','gender','age','Indicators','population','Characteristics']] #Reorders the columns in df3
df3['Indicators'] = df3.Indicators.str.replace(r'(^.*obese.*$)', 'obese') #Renames all the rows in the 'Indicators' field containing the word obese
df3['Indicators'] = df3.Indicators.str.replace(r'(^.*overweight.*$)', 'overweight') #Renames all the rows in the 'Indicators' field containing the word overweight
df3['Indicators'] = df3.Indicators.str.replace(r'(^.*activity.*$)', 'active') #Renames all the rows in the 'Indicators' field containing the word activity
df3['Indicators'] = df3.Indicators.str.replace(r'(^.*Diabetes.*$)', 'inactive') #Renames all the rows in the 'Indicators' field containing the word activity
df3['Indicators'] = df3.Indicators.str.replace(r'(^.*Mood.*$)', 'normal') #Renames all the rows in the 'Indicators' field containing the word activity
df3['gender'] = df3.gender.str.replace(r'(^.*Females.*$)', 'female') #Renames all the rows in the 'Indicators' field containing the word obese
df3['gender'] = df3.gender.str.replace(r'(^.*Male.*$)', 'male') #Renames all the rows in the 'Indicators' field containing the word obese

df3 = df3.sort_values(by=['state/region','gender','Indicators','Characteristics'], ascending = [True, True, False,True])


# Calculate the number of people with normal bmi from obese and weight percentage values
# Calculate the number of people inactive from active people percentage values

a=0
for i in range((len(df3))//10):
    df3.iloc[4+a,6] = ((100-df3.iloc[1+a,6]-df3.iloc[3+a,6])*df3.iloc[0+a,6]//df3.iloc[1+a,6]) #calculates the number of people with normal bmi from the obese and overweight ones taking the percentage into account
    df3.iloc[6+a,6] = ((100-df3.iloc[9+a,6])*df3.iloc[8+a,6]//df3.iloc[9+a,6]) #calculates the number of people inactive taking into account the percentage of active people
    a = a+10



# ----------------- MERGE df3 and df1 on state and gender to create df3_1 -----------------

df3 = df3[~df3.Characteristics.str.contains('Percent')] #drops all the rows containing 'percent' in the 'Characteristics' field
df3 = df3.drop(['zip/FSA','Characteristics'], axis=1)
df3 = df3.rename(columns={'Indicators' : 'indicators'})
df3_1 = pd.merge(df3, df1, how='left', on=['state/region','gender'])



# ----------------- Finalising Canada dataframe: df_CA -----------------

df_CA = df3_1




################## Preparation of the US Dataframe: df_US ##################
#############
########
###


# ----------------- df5 (US_household_income_by_zip.csv) -----------------

df5 = df5[['State_Name','State_ab', 'Zip_Code', 'Lat', 'Lon', 'Mean']] #reduces the database to only 6 fields
df5 = df5.rename(columns={'State_Name': 'state', 'Zip_Code': 'zipcode', 'Lat': 'latitude', 'Lon': 'longitude', 'Mean': 'household'})
df5 = df5.groupby(['state','State_ab','zipcode']).mean()
df5 = df5.reset_index()

# checks if there are duplicated Zip_Code values in df5 (US_household_income_by_zip.csv) and drops eventual duplicates
ids = df5['zipcode']
####print ('Duplicated records in Zip_Code field\n', df5[ids.isin(ids[ids.duplicated()])].sort_values(by=["zip"]))
df5 = df5.drop_duplicates(subset='zipcode', keep=False) #Drops all the rows having duplicated Zip_Code record
df5 = df5.sort_values(by=['state'])



# ----------------- df6 (US_nutrition__physical_activity__and_obesity.csv) -----------------

df6 = df6[df6['YearStart']==2015] #keeps all the rows containing the year 2015. I chose 2015 for 2 reasons:
                                  #1) for consistency with data in Canada database (2015 was the only year available)
                                  #2) because is the year with the most records

df6 = df6[['LocationDesc','Question', 'Data_Value', 'Stratification1']] #reduces the database to only 6 fields
df6 = df6[df6['Question'].str.contains('75 minutes a week of vigorous-intensity aerobic activity|obesity|overweight|vegetables|fruit')]# |leisure-time |vegetables')]
df6 = df6[df6['Stratification1'].str.contains('Male|Female')]
df6 = df6[~df6.LocationDesc.str.contains("National")] #drops all the rows containing , and Canada in the 'GEO' field
df6['Question'] = df6.Question.str.replace(r'(^.*150.*$)', 'active') #Renames all the rows in the 'Indicators' field containing the word activity
df6['Question'] = df6.Question.str.replace(r'(^.*obesity.*$)', 'obese') #Renames all the rows in the 'Indicators' field containing the word activity
df6['Question'] = df6.Question.str.replace(r'(^.*overweight.*$)', 'overweight') #Renames all the rows in the 'Indicators' field containing the word activity
df6['Question'] = df6.Question.str.replace(r'(^.*vegetables.*$)', 'normal') #Renames all the rows in the 'Indicators' field containing the word activity
df6['Question'] = df6.Question.str.replace(r'(^.*fruit.*$)', 'inactive') #Renames all the rows in the 'Indicators' field containing the word activity

df6 = df6.rename(columns={'LocationDesc': 'state', 'Question': 'indicators', 'Data_Value': 'percent', 'Stratification1': 'gender'})
df6 = df6.sort_values(by=['state'])
df6['gender'] = df6['gender'].str.lower()



# ----------------- df7 (US_population_by_zip_2010.csv) -----------------

df7 = df7.dropna(subset=['minimum_age']) #drops all the rows which contains na values in User_Score and Critic_Score columns
df7 = df7[['population','gender', 'zipcode']] #reduces the database to only 3 fields
df7 = df7.groupby(['zipcode','gender']).sum()
df7 = df7.reset_index()



# ----------------- MERGE df5 and df7 on zipcode to create df5_7 -----------------
# ----------------- MERGE df5_7 and df6 on state and gender to create df5_7_6 -----------------

df5_7 = pd.merge(df5, df7, how='left', on=['zipcode'])
df5_7 = df5_7.dropna(subset=['gender']) #drops all the rows which contains na values in User_Score and Critic_Score columns
df5_7_6 = pd.merge(df5_7, df6, how='left', on=['state','gender'])



# calculates the number of people with normal bmi from obese and weight percentage values
# calculates the number of people inactive from active people percentage values

df5_7_6 ['pop_calc'] = df5_7_6.apply(lambda row: row['population'] * row['percent'] /100, axis=1) #it calculates the population of the indicators using the indicators percentage
df5_7_6 = df5_7_6.sort_values(by=['zipcode','gender','indicators'], ascending = [True, True, False])

a=0
for i in range((len(df5_7_6))//5):
    df5_7_6.iloc[2+a,10] = ((100-df5_7_6.iloc[0+a,9]-df5_7_6.iloc[1+a,9])*df5_7_6.iloc[0+a,10]/df5_7_6.iloc[0+a,9]) #calculates the number of people with normal bmi from the obese and overweight ones taking the percentage into account
    df5_7_6.iloc[3+a,10] = ((100-df5_7_6.iloc[4+a,9])*df5_7_6.iloc[4+a,10]/df5_7_6.iloc[4+a,9]) #calculates the number of people inactive taking into account the percentage of active people
    a = a+5



# ----------------- Finalising US dataframe: df_US -----------------

df5_7_6 = df5_7_6.drop(['State_ab', 'population', 'percent'], axis=1)
df5_7_6 = df5_7_6.rename(columns={'pop_calc' : 'population', 'state' : 'state/region', 'zipcode' : 'zip/FSA'})
df5_7_6['country'] = 'United States'
df_US = df5_7_6




################## Preparation of the final dataframe: df_final ##################
#############
########
###


df_final = pd.concat([df_CA, df_US], keys=['x', 'y'], sort=False) #concatenating the 2 dataframe
df_final['age'] = '18 years old or over'
#df_final[['population','household']] = df_final[['population','household']].astype(int)
df_final = df_final.reset_index()
df_final = df_final.drop(['level_0', 'level_1'], axis=1)
df_final = df_final.replace(0, np.nan)
df_final = df_final [['zip/FSA','country','state/region','gender','age','household','indicators','population','latitude','longitude']] #Reorders the columns in df_final
df_final = df_final.rename(columns={'household' : 'household_income'})



################## interactive map ##################
#############
########
###

import folium

graph = df_final [['state/region','latitude','longitude']] #creating a small dataframe with only coordinates
graph = graph.dropna() #remove all nan values
graph = graph.groupby(['state/region']).mean() #group by the 50 states and average the values of coordinates
graph = graph.reset_index()

map = folium.Map(location=[39, -90], zoom_start=3) #creates an empy map centered at 39, -90
graph.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]],radius=7).add_to(map), axis=1)

map.save("interactive_map.html") #saves the map in html



################## Scrubbed dataframes ##################
#############
########
###

#df1.to_csv(r'path\df1.csv') #CA_full_census_by_FSA_code.csv
#df3.to_csv(r'path\df3.csv') #CA_health_by_province.csv
#df5.to_csv(r'path\df5.csv') #US_household_income_by_zip.csv
#df6.to_csv(r'path\df6.csv') #US_nutrition__physical_activity__and_obesity.csv
#df7.to_csv(r'path\df7.csv') #US_population_by_zip_2010.csv

#df_US.to_csv(r'path\df_US.csv') #United States dataframe
#df_CA.to_csv(r'path\df_CA.csv') #Canada dataframe
#df_final.to_csv(r'path\df_final.csv') #final dataframe