# Calling out required packages

import pandas as pd
import seaborn as sns
from scipy import stats

import folium
import numpy as np
import s3fs
import sys
import numpy as np
import time
import re
import pandas as pd
from collections import namedtuple
import dask.dataframe as dd
from tabulate import tabulate

class EDA():
    
    """
    Class for performing EDA for data preprocessing.
    
    Implements different methods to check the quality of data
    A : 
        1 . Number of rows
        2 . Number of columns
        3 . Data type frequency
        4 . Drop_duplicates check
        5 . Check for columns in lower case
        6 . Check whether column names are trimmed
        7 . Check for special characters
    B : 
        1 . Is primary key unique
        2 . Check for missing value in primary key
        
        
    
        
    Parameters
    --------
        df : dataframe
            A dataset with observations in the rows and features in the columns
        path_ : Data path
        prim_key : Primary key for data check    
        
    Attributes
    --------
    
    
    
    
    Notes
    --------
    
        
    
    
    """
    ################################################################################################
    def __init__(self):
#         self.path_ = path_
        # Dataset
#         self.df = read_table(path_)
        pass
        
        
    ################################################################################################
        
    def read_table(self,path_,sep=None):
        
        self.sep = sep
        self.path_ = path_
    
        if '.csv' in self.path_:
            func_ = pd.read_csv
        elif '.parquet' in self.path_:
            func_ = pd.read_parquet
        else:
            func_ = pd.read_csv

        if sep == None:
            for sep in [',','|','\t','\n',';']:
                try:
                    dat = func_(self.path_,sep,dtype='object')
                    break
                except:
                    try:
                        dat = func_('s3://'+self.path_,sep,dtype='object')
                        break
                    except:
                        try:
                            dat = func_(self.path_,sep,dtype='object')
                            break
                        except:
                            try:
                                dat = func_('s3://'+self.path_)
                                break
                            except:
                                pass

        else:
            try:
                dat = func_(self.path_,sep)
            except:
                dat = func_('s3://'+self.path_,sep,dtype='object')

        return dat
    
    ##########################################################################################################
    def data_check(self,df):
        # 1 Number of rows 
        # 2 Number of columns
        # 3 Data type frequency
        # 4 Drop_duplicates check
        # 5 Check for columns in lower case
        # 6 Check whether column names are trimmed
        # 7 Checking for special characters in column names
        ######################################################################################################
        self.df = df
        
        print ('1 . Number of rows : %d ' %(df.shape[0]))  
        print('\n')
        ########################################################################################
        print ('2 . Number of columns : %d ' %(df.shape[1]))
        print('\n')
        ########################################################################################
        print('3 . Data Type Frequency: \n')
        d = pd.value_counts(df.dtypes).to_frame().reset_index()
        
        print(tabulate(d, ['Data Type','Count'],tablefmt="fancy_grid"))
        

        print('\n')
        
    
         # Check for columns in lower case
        if df.columns.str.islower().sum() == df.shape[1]:
            print('4 . All columns are in lower case')
        else :
            print('4 . All columns are not in lower case -------> Making it into lower case')
            df.columns = df.columns.str.lower()
        print('\n')

              
        # Check whether column names are trimmed

        l = [i for i in df.columns if ' ' in i ]
        if len(l) == 0:
            print('5 . All column names are trimmed' )
            
        else :    
            print('5 . All column names are not trimmed ')
            print('\t','Un-trimmed Columns : ',l)
            print('\n')
            print('\t','Correct Format : ')

            for i in l:        
                print('\t',i,' => ',i.strip())

            print('\n')
            print('\t','\t','For Ref. , Run : data_new = eda.trim(data)')

        print('\n')
        ########################################################################################
        ########################################################################################
        ########################################################################################
        print('6. Checking for special characters in column names : ')
        print('\n')
        counter = 0
        old  =[]
        new = []
        dictionary = {}
        for i in df.columns:
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')

            if(regex.search(str(i)) != None):
                counter = counter + 1
                s = re.findall("[@!#$%^&*()<>?/\|}{~:]", str(i))

                old_str = i
                new_str = re.sub('[^A-Za-z0-9]+', '_', i)
                old.append(old_str)
                new.append(new_str)

                print('\t Col : %s'%(i))
                print('\t', 'Status : String is not accepted')
                print('\t Special Character/s : %s' %(s))
                print('\n')


        if counter == 0:
            print('\t','None of the column names contain special characters')
        else:
            dictionary = dict(zip(old, new))
            for key,val in dictionary.items():
                print('\t',key, " : ", val,'\n')
            print('\t','Dictionary for Renaming Column Names : ' , dictionary)
            print('\n')
            print('\t','\t','For Ref, run :  data_new = eda.special_char(data)') 


        print('\n') 

        return df
    
     ############################################################################################
    def primary_key_check(self,df,prim_key):
        prim_key = prim_key
        
        # Primary Key Unique Count
        # Is primary key unique
        # missing value in primary key
        # Frequency table of Primary Key length
        print('1 . Unique Count ( Primary Key ) : ' , df[prim_key].nunique())
        print('\n')
        ########################################################################################
        # Is primary key unique
    
        if (df[prim_key].nunique()!= df.shape[0]) :
            print('2 . Duplicate Primary Key is present')
        else:
            print('2 . Duplicate Primary Key is not present')
        print('\n')  
        
        ########################################################################################
        # missing value in primary key
        
        if (df[prim_key].isnull().sum() > 0 ) :
            print('3 . Primary Key have missing values')
            print('\t','Null Count : ' ,df[prim_key].isnull().sum())
        else:
            print('3 . Primary Key does not have missing values')

        
        print('\n')
        print('4 . Frequency table of Primary Key length')
        counts = df[prim_key].apply(lambda x : len(str(x))).value_counts().to_frame()
        print(tabulate(counts, ['KEY Length','Count'],tablefmt="fancy_grid"))        
        print('\n')
        
    ############################################################################################    
    def date_check(self,df):
        # Date cols and their entries
        print('Date cols and their entries:')
        print('\n')
        date = [i for i in df.columns if 'DATE' in i ]
        _dt = [i for i in df.columns if '_DT' in i ]
        dt = [i for i in df.columns if 'DT' in i ]
        col_dt = list(set(date) | set(_dt)| set(dt))
        for i in col_dt:
            if df[i].nunique()>5:
                l = df[i].unique()[3]
                if len(l)<20 :
                    print ('\t',i ,' : %s ' %(l))
        print('\n')  
        
    def trim(self,df):
        self.df = df
        # Check whether column names are trimmed
        
        l = [i for i in df.columns if ' ' in i ]
        if len(l) == 0:
            print('All column names are trimmed' )
            
        else :
            print('All column names are not trimmed ')
            print('\t','Un-trimmed Columns : ',[i for i in df.columns if ' ' in i ])
            print('\n')

            df.columns = df.columns.str.strip()
            l = [i for i in df.columns if ' ' in i ]

            if len(l) == 0:
                print('\t','Data has been returned with trimmed columns' )

        print('\n')


        return df
    ####################################################################################
    def special_char(self , df , str_to_replace):
    
        self.df = df
        self.str_to_replace = str_to_replace
        
        counter = 0
        old  =[]
        new = []
        dictionary = {}
        for i in df.columns:
            regex = re.compile('[@!#$%^&*()<>?/\|}{~:]')

            if(regex.search(str(i)) != None):
                counter = counter + 1
                s = re.findall("[@!#$%^&*()<>?/\|}{~:]", str(i))

                
                new_str = re.sub('[@!#$%^&*()<>?/\|}{~:]', str_to_replace , i)
                new_str = new_str.strip()
                
                old.append(i)
                new.append(new_str)

        if counter == 0:
            print('\t','None of the column names contain special characters')
        else:
            dictionary = dict(zip(old, new))
            print('\t',' Renamed Columns : ' )
            for key,val in dictionary.items():
                print('\t',key, " => ", val,'\n')
            
            

        df = df.rename(columns = dictionary )
        print('\n')
        print('\t','Data has been returned after eliminating special characters from columns' )
        print('\n') 
        return df
    #######################################################################################
    def target_check(self , df , target):
    
        self.df = df
        self.target = target
        
        print('Target Null Count: ',df[target].isnull().sum() )
        print('\n')
        
        print('Target Value count :')
        d = pd.value_counts(df[target]).to_frame().reset_index()
        print(tabulate(d, tablefmt='psql'))
              
        print('\n')
        print('Data Type :')
        print(d.dtypes)
        
    ###########################################################################################################
    def duplicate_check(self , df , lst):
        self.df = df
        self.lst = lst
        ########################################################################################
        # Checking for drop_duplicates
        if (df.shape[0] == df.drop_duplicates().shape[0]) == True :
                    print('Duplicate rows are not present in full data')
        else:
            print('Duplicate rows are present in full data')

        print ('\tNumber of duplicate rows : %s  \n' %(df[df.duplicated(keep=False)].shape[0])) 
        
        if isinstance(lst, list)==True :
            if len(lst) == 0:
                pass
            else:
                if (df.shape[0] == df.drop_duplicates(subset=lst).shape[0]) == True :
                    print('\t Duplicate rows are not present on the basis of : ', lst)
                else:
                    print('\t Duplicate rows are present on the basis of ', lst)
                    
                print ('\t Number of duplicate rows : %s  \n' %(df[df.duplicated(subset = lst, keep=False)].shape[0]))        

            
            print('\n')  
        else:
            print('Check whether argument is df and list ')
            print('\n')
       
            