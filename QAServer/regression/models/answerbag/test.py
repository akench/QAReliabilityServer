# coding: utf-8

# ### Importing all the necessary libraries and packages

# In[51]:

import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import pickle
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score,accuracy_score,classification_report
from sklearn import model_selection


# ## Enter this path where test data, mmachine learning models are stored

# In[127]:

path=input('Enter Path for the data: ')
#Path name


# ### Below script loads the machine learning models into memory

# In[79]:

Clear_filename=path+'Clear_model.sav'
Clear_model = pickle.load(open(Clear_filename, 'rb'))
Credible_filename=path+'Credible_model.sav'
Credible_model = pickle.load(open(Credible_filename, 'rb'))
Complete_filename=path+'Complete_model.sav'
Complete_model = pickle.load(open(Complete_filename, 'rb'))
Correct_filename=path+'Correct_model.sav'
Correct_model = pickle.load(open(Correct_filename, 'rb'))


# In[72]:

# This is used to get the column names to be used for the testing data
X_Clear=['avg_word_sentence', 'num_misspelled', 'bin_taboo', 'grammar_check',
                'Subjectivity']
X_Credible=['avg_word_sentence', 'num_misspelled','bin_taboo','Polarity']
X_Complete=['Average IDF', 'Entropy', 'Polarity',
       'Subjectivity']
X_Correct=['grammar_check', 'num_mispelled','Polarity']


# ## Importing Test Data
# #### Format to be used to load the testing data
# 1. Test data has to be in excel format
# 2. Name of the file should be testing_data to avoid unnecessary changes
# 3. Test data should be stored in the same folder where machine learning models are stored

# In[73]:

testing_data = pd.read_excel(path+'testing_data.xlsx')


# <b> This function has following arguments: </b>
# 1. X --> X takes a list of columns for each 4 outputs like Clear,Complete etc
# 2. Y --> It is used to name the variables for each 4 outputs like Clear,Complete etc
# 3. output_data --> this takes a dataframe as input
# 4. percentile --> currently the confidence intervals is set at 95
# 5. model --> this takes the name of the machine learning model for which operations are performed

# In[121]:

def test_function(X,Y='Clear_1',output_data=testing_data,percentile=95,model=Clear_model):
    col=X
    ntest=output_data[output_data.columns.difference(['Answers'])]
    ntest=pd.get_dummies(ntest)
    ntest=ntest[col]
    allTree_preds = np.stack([t.predict(ntest) for t in model.estimators_], axis = 0)
    err_down = np.round(np.percentile(allTree_preds, (100 - percentile) / 2.0  ,axis=0),2)
    err_up = np.round(np.percentile(allTree_preds, 100- (100 - percentile) / 2.0  ,axis=0),2)
    ci = err_up - err_down
    yhat = model.predict(ntest)
    df = pd.DataFrame()
    a=Y+'_down'
    b=Y+'_up'
    c=Y+'_deviation'
    df[a] = err_down
    df[b] = err_up
    df[Y] = yhat
    df[c] = (df[b] - df[a])/df[Y]
    predic=output_data.merge(df,left_index=True,right_index=True)
    return predic


# In[122]:

clear_data=test_function(X=X_Clear,Y='Clear_1',model=Clear_model,output_data=testing_data)
complete_data=test_function(X=X_Complete,Y='Complete_1',model=Complete_model,output_data=clear_data)
credible_data=test_function(X=X_Credible,Y='Credible_1',model=Credible_model,output_data=complete_data)
correct_data=test_function(X=X_Correct,Y='Correct_1',model=Correct_model,output_data=credible_data)


# <b>This function takes the predicted output value and converts into a range from 0-100</b>

# In[123]:

def calc_percent(df,text):
    ma=max(df[text])
    mi=min(df[text])
    a=text+'_down'
    b=text+'_up'
    r = df[b] - df[a]
    #correctedStartValue = df[text] - df[]
    col=text+' %'
    df[col] = (round(r,2) * 100) / df[b]


# In[124]:

calc_percent(correct_data,'Correct_1')
calc_percent(correct_data,'Credible_1')
calc_percent(correct_data,'Complete_1')
calc_percent(correct_data,'Clear_1')


# In[125]:

# Creating final data with only the predicted confidence intervals and percentage values
final_data=correct_data[['Clear_1_down', 'Clear_1_up','Clear_1 %',
       'Credible_1_down', 'Credible_1_up','Credible_1 %',
       'Complete_1_down', 'Complete_1_up','Complete_1 %',
         'Correct_1_down', 'Correct_1_up','Correct_1 %']]


# In[129]:

final_data.to_excel(path+'regression_output_final.xlsx',index=False)