
# coding: utf-8

# ### importing necessary packages

# In[2]:

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# get_ipython().magic('matplotlib inline')


# In[3]:

xls=pd.ExcelFile('./regression_Q&A.xlsx')


# In[4]:

training = pd.read_excel(xls, 'training')


# In[5]:

training.head(2)


# In[6]:

training.shape


# In[7]:

del training['Answers']


# In[7]:

training.columns


# In[8]:

training.dtypes


# In[9]:

## Check for null values in data


# In[10]:

pd.isnull(training).sum()
# reputation has total 10 records which are null


# In[8]:

## filling 0 value to correct_l column
#training.loc[training['reputation']].fillna('', inplace=True)
training.reputation = training.reputation.fillna('')


# ### checking for any duplicate records

# In[12]:

training[training.duplicated(keep=False)]


# #### no duplicate entries

# In[13]:

## Converting reputation variable from text to numeric for model


# In[9]:

training=pd.get_dummies(training)
training.columns


# ### Creating four different dataframes

# In[10]:

Clear=training[['rating', 'num_upvotes', 'avg_word_sentence', 'num_misspelled', 'bin_taboo', 'grammar_check',
                'Subjectivity', 'Clear_l','reputation_Ace','reputation_Ambitious', 'reputation_Beginner',
       'reputation_Brainly User', 'reputation_Expert', 'reputation_Genius','reputation_Helping Hand', 'reputation_Virtuoso']] 
Credible=training[['rating','num_thanks','avg_word_sentence', 'num_misspelled','bin_taboo','Polarity','Credible_l',
                  'reputation_Ace',
       'reputation_Ambitious', 'reputation_Beginner',
       'reputation_Brainly User', 'reputation_Expert', 'reputation_Genius',
       'reputation_Helping Hand', 'reputation_Virtuoso']]
Complete=training[['rating','num_upvotes', 'num_thanks','Average IDF', 'Entropy', 'Polarity',
       'Subjectivity','Complete_l',
                  'reputation_Ace',
       'reputation_Ambitious', 'reputation_Beginner',
       'reputation_Brainly User', 'reputation_Expert', 'reputation_Genius',
       'reputation_Helping Hand', 'reputation_Virtuoso']]
Correct=training[['rating','num_upvotes', 'num_thanks','Polarity','Correct_l',
                 'reputation_Ace',
       'reputation_Ambitious', 'reputation_Beginner',
       'reputation_Brainly User', 'reputation_Expert', 'reputation_Genius',
       'reputation_Helping Hand', 'reputation_Virtuoso']]


# In[11]:

# Output values
print(Clear['Clear_l'].unique())
print(Complete['Complete_l'].unique())
print(Correct['Correct_l'].unique())
print(Credible['Credible_l'].unique())


# In[ ]:




# In[12]:

from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score,accuracy_score,classification_report
from sklearn import model_selection


# In[13]:

X_Clear=Clear[Clear.columns.difference(['Clear_l'])]
Y_Clear=Clear['Clear_l']
X_Credible=Credible[Credible.columns.difference(['Credible_l'])]
Y_Credible=Credible['Credible_l']
X_Complete=Complete[Complete.columns.difference(['Complete_l'])]
Y_Complete=Complete['Complete_l']
X_Correct=Correct[Correct.columns.difference(['Correct_l'])]
Y_Correct=Correct['Correct_l']


# In[14]:

def train_test(X,Y,test_size):
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state=25)
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test=train_test(X_Clear,Y_Clear,test_size=0.3)


# In[15]:

def fit_model(model,X_train, X_test, y_train, y_test):
    ml_model=model
    result=ml_model.fit(X_train,y_train)
    prediction=result.predict(X_test)
    return prediction,result


# ### regression using RandomForest trees

# In[25]:

prediction,result=fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)


# In[26]:

r2_score(prediction,y_test)


# In[ ]:




# In[27]:

mean_squared_error(prediction,y_test)


# ## Performing Cross-validation

# In[28]:

def cross_validation(model):
    kfold = model_selection.KFold(n_splits=10, random_state=7)
    modelCV = model
    scoring = 'neg_mean_squared_error'
    results=(model_selection.cross_val_score(modelCV, X_Clear, Y_Clear, cv=kfold, scoring=scoring))
    a=(results.mean())
    return -a


# In[29]:

cross_validation(RandomForestRegressor())


# <b> 1. The MSE after CV is 1.98 against our model having 1.66. <b> 
# 
# <b> 2. Hence we can confirm that the model train test split is proper <b> 

# ## Reading our test data and predicting the scores for Clear

# In[30]:

test = pd.read_excel(xls, 'testing')


# In[31]:

test.head(1)


# ## Function to calculate Confidence Interval and Prediction on Tested Data

# In[32]:

def test_func(X,Y='Clear_1',op=test,percentile=95):
    col=X.columns
    ntest=test[test.columns.difference(['Answers'])]
    ntest=pd.get_dummies(ntest)
    ntest=ntest[col]
    
    allTree_preds = np.stack([t.predict(ntest) for t in result.estimators_], axis = 0)
    
    err_down = np.percentile(allTree_preds, (100 - percentile) / 2.0  ,axis=0)
    err_up = np.percentile(allTree_preds, 100- (100 - percentile) / 2.0  ,axis=0)
    
    ci = err_up - err_down
    yhat = result.predict(ntest)
    y = y_test
    
    df = pd.DataFrame()
    a=Y+'_down'
    b=Y+'_up'
    c=Y+'_deviation'
    df[a] = err_down 
    df[b] = err_up
    df[Y] = yhat
    df[c] = (df[b] - df[a])/df[Y]
    #df.reset_index(inplace=True)
    #df_sorted = df.iloc[np.argsort(df['deviation'])[::-1]]
    predic=op.merge(df,left_index=True,right_index=True)
    return predic


# In[34]:

sd=test_func(X=X_Clear,Y='Clear_1')


# In[35]:

sd.head(1)


# # Building model on Credible

# In[36]:

X_train, X_test, y_train, y_test=train_test(X_Credible,Y_Credible,test_size=0.3)
prediction,result=fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)


# In[37]:

r2_score(prediction,y_test)


# In[38]:

mean_squared_error(prediction,y_test)


# ### The MSE is low which is a good

# ## Testing the model on unseen data

# In[39]:

cred_data=test_func(X=X_Credible,Y='Credible_1',op=sd)
#sd=test_func(X=X_Clear,Y='Clear_1')


# # Building model on Complete

# In[40]:

X_train, X_test, y_train, y_test=train_test(X_Complete,Y_Complete,test_size=0.3)
prediction,result=fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)


# In[41]:

r2_score(prediction,y_test)


# In[42]:

mean_squared_error(prediction,y_test)


# ## Almost similar MSE when compared to Clear and similar R2

# ## testing this model on unseen data

# In[43]:

complete_data=test_func(X=X_Complete,Y='Complete_1',op=cred_data)


# # Building model on Correct

# In[44]:

X_train, X_test, y_train, y_test=train_test(X_Correct,Y_Correct,test_size=0.3)
prediction,result=fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)
print('The r2 of model is ',r2_score(prediction,y_test))
print('MSE of this model is ',mean_squared_error(prediction,y_test))


# ## testing this model on unseen data

# In[45]:

final=test_func(X=X_Correct,Y='Correct_1',op=complete_data)


# In[46]:

final.head(2)


# In[47]:

final.shape


# In[48]:

def calc_range(df,text):
    ma=max(final[text])
    mi=min(final[text])
    r = ma - mi
    correctedStartValue = final[text] - mi
    col=text+' %'
    df[col] = (correctedStartValue * 100) / r


# In[49]:

calc_range(final,'Correct_1')


# In[50]:

calc_range(final,'Complete_1')


# In[51]:

calc_range(final,'Credible_1')


# In[52]:

calc_range(final,'Clear_1')


# In[53]:

final.to_excel('./regression_output.xlsx',index=False)

