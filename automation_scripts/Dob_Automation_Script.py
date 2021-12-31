import pandas as pd
import numpy as np
import datetime
import time


def collect_dob_data(previous_month):
    results_df = pd.read_csv("https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=500000&$where=date_trunc_ym(created_date)='%s-01T00:00:00.000'" % previous_month)

    names = ["BOROUGH", 'Bin #', 'House #', 'Street Name', 'Job #', 'Job doc. #',
       'Job Type', 'Self_Cert', 'Block', 'Lot', 'Community Board', 'Zip Code',
       'Bldg Type', 'Residential', 'Special District 1', 'Special District 2',
       'Work Type', 'Permit Status', 'Filing Status', 'Permit Type',
       'Permit Sequence #', 'Permit Subtype', 'Oil Gas', 'Site Fill',
       'Filing Date', 'Issuance Date', 'Expiration Date', 'Job Start Date',
       "Permittee's First Name", "Permittee's Last Name",
       "Permittee's Business Name", "Permittee's Phone #",
       "Permittee's License Type", "Permittee's License #",
       'Act as Superintendent', "Permittee's Other Title", 'HIC License',
       "Site Safety Mgr's First Name", "Site Safety Mgr's Last Name",
       'Site Safety Mgr Business Name', 'Superintendent First & Last Name',
       'Superintendent Business Name', "Owner's Business Type", 'Non-Profit',
       "Owner's Business Name", "Owner's First Name", "Owner's Last Name",
       "Owner's House #", "Owner's House Street Name", "Owner’s House City'",
       "Owner’s House State", "Owner’s House Zip Code", Owner's Phone #,
       'DOBRunDate', 'PERMIT_SI_NO', 'LATITUDE', 'LONGITUDE',
       'COUNCIL_DISTRICT', 'CENSUS_TRACT', 'NTA_NAME']

    results_df.columns = names

    empty_lon_and_lat = results_df[results_df["LONGITUDE"].isna()]
    empty_lon_and_lat_nozip = empty_lon_and_lat[empty_lon_and_lat["Zip Code"].notna()]

    # Importing the Nominatim geocoder class
    from geopy.geocoders import Nominatim

    # address we need to geocode
    loc = '1 BROOKLYN PLAZA, New York, 11201'

    # making an instance of Nominatim class
    geolocator = Nominatim(user_agent="my_request")

    # applying geocode method to get the location
    location = geolocator.geocode(loc, timeout=10)


    df=empty_lon_and_lat_nozip
    df['Zip Code'] = df["Zip Code"].astype(int)
    df["Address"] = df["House #"].astype(str) +" " + df["Street Name"] + ", " + df['BOROUGH'] + ", New York" + ", "+df["Zip Code"].astype(str)
    geolocator = Nominatim(user_agent="my_request")
    for index, row in df.iterrows():
        loc = row['Address']
        #making an instance of Nominatim class
        #applying geocode method to get the location
        location = geolocator.geocode(loc, timeout=10)
        try:
            location.address
            #print(location.address)
      #printing address and coordinates
            df.loc[index,'LATITUDE'] = location.latitude
            df.loc[index,'LONGITUDE'] = location.longitude
        except:
            pass

    lon_lat_not_empty = results_df
    new_df = lon_lat_not_empty.append(df)
    clean_df = new_df[~new_df.index.duplicated(keep='last')]
    final_df = clean_df.sort_index()

    final_df = final_df[["BOROUGH",'Job Type', 'Block', 'Lot',  'Zip Code', 'Work Type',
         'Permit Status', 'Filing Status', 'Permit Type', 'Permit Subtype',
       'Filing Date', 'Issuance Date', 'Expiration Date', 'Job Start Date','LATITUDE', 'LONGITUDE',
       'COUNCIL_DISTRICT', 'CENSUS_TRACT', 'NTA_NAME']]
    final_df['Issuance Date'] = pd.to_datetime(final_df['Issuance Date'])
    final_df['year'] = final_df['Issuance Date'].dt.year.fillna(0.0).astype(int)
    final_df = final_df[final_df['year'] > 1999]
    final_df = final_df.replace(["MANHATTAN", "BRONX", "BROOKLYN", "QUEENS", "STATEN ISLAND"], value = [1,2,3,4,5])
    final_df['Block'] = final_df['Block'].astype(str)
    final_df['Lot'] = final_df['Lot'].astype(str)
    final_df['Block'] = final_df['Block'].replace({r'.0':''}, regex =True)
    final_df['Lot'] = final_df['Lot'].replace({r'.0':''}, regex =True)
    final_df['BBL'] = final_df['BOROUGH'].astype(str)+ final_df['Block'].str.zfill(5) + final_df['Lot'].str.zfill(4)



if __name__ == "__main__":
    # previous_month = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime('%Y-%m')
    # previous_month can be changed to any month of preference, e.g. '2018-01'
    previous_month = '2011-01'
    final_df = collect_dob_data(previous_month)
    final_df.to_csv('dob_data.csv')
