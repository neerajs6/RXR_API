import pandas as pd
import numpy as np
import tensorflow as tf
import datetime
import time
import pickle

from transformers import BertTokenizer, BertModel, TFPreTrainedModel
from transformers import AutoTokenizer, pipeline, TFDistilBertModel, TFBertModel
from sentence_transformers import SentenceTransformer
import tensorflow as tf
import os
import random

import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, MetaData
engine = sqlalchemy.create_engine('mysql://admin:RxR12345@database-1.cbhzog3pc3ub.us-east-2.rds.amazonaws.com:3306/RxR') # connect to SQL database

def fix_zip(input_zip):
    try:
        input_zip = int(float(input_zip))
    except:
        try:
            input_zip = int(input_zip.split('-')[0])
        except:
            return np.NaN
    if input_zip < 10000 or input_zip > 12000:
        return np.NaN
    return str(input_zip)

def clean_date(date):
    try:
        if(np.all(pd.notnull(date))):
            return datetime.datetime.strptime(date,'%m/%d/%Y %I:%M:%S %p')
        else:
            return np.nan
    except:
        return np.nan

def collect_311_data(previous_month):
    df = pd.read_csv("https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$limit=500000&$where=date_trunc_ym(created_date)='%s-01T00:00:00.000'" % previous_month)
    
    # Drop irrelevant columns
    df.drop(columns=['address_type','facility_type','due_date','resolution_description',\
                            'resolution_action_updated_date','community_board','vehicle_type',\
                            'taxi_company_borough','taxi_pick_up_location','bridge_highway_name',\
                            'bridge_highway_direction','road_ramp','bridge_highway_segment',\
                            'location'],inplace=True)   
  
    # Create a new var coordinates
    df['coordinates'] = df[['longitude', 'latitude']].apply(list, axis=1)
   
    # Clean zip codes, remove rows where zip codes are null
    df['incident_zip'] = df['incident_zip'].apply(fix_zip)
    df = df[df['incident_zip'].notnull()]
    
    # Remove rows where latitude and longitude are null
    df = df[(df['latitude'].notnull()) & (df['longitude'].notnull())]

    # Drop rows with Unspecified borough
    df = df[df['borough'] != 'Unspecified']

    # Create new variable ctype -- used to create embeddings afterwards
    df['ctype'] = df['complaint_type'] + " " + df['descriptor']
    
    # Change dates from str to Timestamp object
    df['created_date']= df['created_date'].str.replace('T',' ')
    df['created_date']= df['created_date'].str[:-4]
    df['created_date']= df['created_date'].apply(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S'))

    df['closed_date']= df['closed_date'].str.replace('T',' ')
    df['closed_date']= df['closed_date'].str[:-4]
    df['closed_date']= df['closed_date'].apply(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S') if(np.all(pd.notnull(x))) else x)
   
    # Convert BBL to str
    df = df[~df['bbl'].isnull()]
    df['bbl']=df['bbl'].astype(str).str[:-2]
   
    # Create variables for year and month
    df['year'] = df['created_date'].dt.year
    df['month'] = df['created_date'].dt.month
    df['ctype']=df['ctype'].str.lower()

    df['ctype_lower'] = df['ctype'].str.lower()
    
    df=df.rename(columns={'created_date':'CREATED_DATE', 'closed_date':'CLOSED_DATE', 'agency':'AGENCY', \
                          'agency_name':'AGENCY_NAME','complaint_type':'COMPLAINT_TYPE', 'descriptor':'DESCRIPTOR', \
                          'location_type':'LOCATION_TYPE', 'incident_zip':'INCIDENT_ZIP','incident_address':'INCIDENT_ADDRESS',\
                          'street_name':'STREET_NAME', 'cross_street_1':'CROSS_STREET_1', 'cross_street_2':'CROSS_STREET_2',\
                          'intersection_street_1':'INTERSECTION_STREET_1', 'intersection_street_2':'INTERSECTION_STREET_2',\
                          'city':'CITY', 'landmark':'LANDMARK','status':'STATUS', 'borough':'BOROUGH',\
                          'x_coordinate_state_plane':'X_COORD_STATE_PLANE','y_coordinate_state_plane':'Y_COORD_STATE_PLANE',\
                          'open_data_channel_type':'OPEN_DATA_CHANNEL_TYPE','park_facility_name':'PARK_FACILITY_NAME',\
                          'park_borough':'PARK_BOROUGH', 'latitude':'LATITUDE', 'longitude':'LONGITUDE','year':'YEAR',\
                          'month':'MONTH','ctype':'CTYPE','ctype_lower':'CTYPE_LOWER','bbl':'BBL','unique_key':'UNIQUE_KEY'})
    df.to_csv(str(previous_month)+'.csv',index=False)
    #df.astype(str).to_sql(name='311_cleaned_data', con=engine, index=False, if_exists='append')

    print("DATA PROCESSING FOR "+previous_month+" COMPLETED")
    ### THIS SHOULD BE SAVED TO 311_CLEANED DATA
    return df

def bert_base_embedding(input_list):
  tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/bert-base-nli-mean-tokens')
  model = SentenceTransformer('bert-base-nli-mean-tokens')
  word_embeddings = model.encode(input_list, show_progress_bar=True)
  return word_embeddings

if __name__ == "__main__":
    # previous_month = (datetime.datetime.now()-datetime.timedelta(days=30)).strftime('%Y-%m')
    # previous_month can be changed to any month of preference, e.g. '2018-01'
    previous_month = '2011-01'
    processed_data = collect_311_data(previous_month)

    model = SentenceTransformer('bert-base-nli-mean-tokens')
    kclusterer = pickle.load(open("kclusterer.pkl", "rb"))

    text_df = processed_data[['COMPLAINT_TYPE','DESCRIPTOR','CTYPE','CTYPE_LOWER']]
    text_df = text_df.drop_duplicates()
    text_df = text_df.dropna()
    base_complaint_embedding = bert_base_embedding(text_df['CTYPE_LOWER'].unique())
    assigned_clusters=list()
    for i in range(len(base_complaint_embedding)):
        assigned_clusters.append(kclusterer.classify(base_complaint_embedding[i]))
    data_cl_bert = pd.DataFrame(list(zip(text_df['CTYPE_LOWER'].unique(),assigned_clusters)),columns=['CTYPE_LOWER','CLUSTER'])
    data_cl_bert['EMBEDDING']=list(base_complaint_embedding)
    data_cl_bert = data_cl_bert.reset_index()
    data_cl_bert = data_cl_bert.rename(columns={'index':"INDEX"})
    data_cl_bert.to_csv('sample_embeddings.csv',index=False)
    #data_cl_bert.astype(str).to_sql(name='311_embeddings', con=engine, index=False, if_exists='append')
    ### THIS SHOULD BE SAVED TO 311_EMBEDDINGS
    
    # Use the model to predict clusters
    processed_data = processed_data[['CREATED_DATE','BBL','COMPLAINT_TYPE','DESCRIPTOR','CTYPE','YEAR','MONTH','CTYPE_LOWER']]
    df_join = pd.merge(processed_data,data_cl_bert,how='left',left_on='CTYPE_LOWER',right_on='CTYPE_LOWER')
    cluster_dummies = pd.get_dummies(df_join['CLUSTER'])
    df_join = pd.concat([df_join,cluster_dummies],axis=1)
    grouped_by_year_bbl = df_join.groupby(['YEAR','BBL'])[0.0,1.0,2.0,3.0,4.0,5.0].sum()
    grouped_by_year_bbl['TOTAL'] = grouped_by_year_bbl.sum(axis=1)
    grouped_by_year_bbl_reset=grouped_by_year_bbl.reset_index()
    index = pd.MultiIndex.from_tuples(((yr, bbl) for yr in list(grouped_by_year_bbl_reset['YEAR'].unique()) for bbl in grouped_by_year_bbl_reset['BBL']), names=["YEAR", "BBL"])
    final_df = pd.DataFrame(index=index, columns=[0.0,1.0,2.0,3.0,4.0,5.0,'TOTAL'])
    final_df.update(grouped_by_year_bbl)
    final_df = final_df.replace(np.nan,0)
    final_df.to_csv('311_model_input.csv')
