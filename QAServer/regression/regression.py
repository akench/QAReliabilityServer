import numpy as np
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score,accuracy_score,classification_report
from sklearn import model_selection

CLEAR_FILENAME = "QAServer/regression/models/{}/Clear_model.sav"
CREDIBLE_FILENAME = "QAServer/regression/models/{}/Credible_model.sav"
COMPLETE_FILENAME = "QAServer/regression/models/{}/Complete_model.sav"
CORRECT_FILENAME = "QAServer/regression/models/{}/Correct_model.sav"

def get_models(model_name):
    # Below script loads the machine learning models into memory
    Clear_filename = CLEAR_FILENAME.format(model_name)
    Clear_model = pickle.load(open(Clear_filename, 'rb'))
    Credible_filename = CREDIBLE_FILENAME.format(model_name)
    Credible_model = pickle.load(open(Credible_filename, 'rb'))
    Complete_filename = COMPLETE_FILENAME.format(model_name)
    Complete_model = pickle.load(open(Complete_filename, 'rb'))
    Correct_filename = CORRECT_FILENAME.format(model_name)
    Correct_model = pickle.load(open(Correct_filename, 'rb'))

    return Clear_model, Credible_model, Complete_model, Correct_model

# In[72]:
class BrainlyModels():
    # This is used to get the column names to be used for the testing data
    X_Clear =       ['rating', 'num_upvotes', 'avg_word_sentence', 'num_misspelled', 
                    'bin_taboo', 'grammar_check', 'Subjectivity']
    X_Credible =    ['rating','num_thanks','avg_word_sentence', 'num_misspelled',
                    'bin_taboo','Polarity']
    X_Complete =    ['rating','num_upvotes', 'num_thanks','Average IDF', 
                    'Entropy', 'Polarity', 'Subjectivity']
    X_Correct =     ['rating','num_upvotes', 'num_thanks','Polarity']

    Clear_model, Credible_model, Complete_model, Correct_model = get_models('brainly')

class AnswerbagModels():
    # This is used to get the column names to be used for the testing data
    X_Clear =       ['avg_word_sentence', 'num_misspelled', 'bin_taboo', 
                    'grammar_check', 'Subjectivity']
    X_Credible =    ['avg_word_sentence', 'num_misspelled','bin_taboo','Polarity']
    X_Complete =    ['Average IDF', 'Entropy', 'Polarity', 'Subjectivity']
    X_Correct =     ['grammar_check', 'num_mispelled','Polarity']

    Clear_model, Credible_model, Complete_model, Correct_model = get_models('answerbag')

# <b> This function has following arguments: </b>
# 1. X --> X takes a list of columns for each 4 outputs like Clear,Complete etc
# 2. Y --> It is used to name the variables for each 4 outputs like Clear,Complete etc
# 3. output_data --> this takes a dataframe as input
# 4. percentile --> currently the confidence intervals is set at 95
# 5. model --> this takes the name of the machine learning model for which operations are performed

# In[121]:

def test_function(X, Y, model, output_data, percentile=95):
    col = X
    ntest = output_data[output_data.columns.difference(['Answers'])]
    # print(ntest)
    ntest = pd.get_dummies(ntest)
    # print(ntest)
    ntest = ntest[col]
    allTree_preds = np.stack([t.predict(ntest) for t in model.estimators_], axis = 0)
    err_down = np.round(np.percentile(allTree_preds, (100 - percentile) / 2.0  ,axis=0),2)
    err_up = np.round(np.percentile(allTree_preds, 100- (100 - percentile) / 2.0  ,axis=0),2)
    ci = err_up - err_down
    yhat = model.predict(ntest)
    df = pd.DataFrame()
    a = Y + '_down'
    b = Y + '_up'
    c = Y + '_deviation'
    df[a] = err_down
    df[b] = err_up
    df[Y] = yhat
    df[c] = (df[b] - df[a])/df[Y]
    predic=output_data.merge(df,left_index=True,right_index=True)
    return predic

# <b>This function takes the predicted output value and converts into a range from 0-100</b>

# In[123]:

def calc_percent(df,text):
    ma = max(df[text])
    mi = min(df[text])
    a = text+'_down'
    b = text+'_up'
    r = df[b] - df[a]
    #correctedStartValue = df[text] - df[]
    col = text+' %'
    df[col] = (round(r,2) * 100) / df[b]