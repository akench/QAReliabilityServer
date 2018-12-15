
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score,accuracy_score,classification_report
from sklearn import model_selection

# SkLearn gives a bunch of warnings that models and such will change
# in the future. There is no intent to use the imported modules
# differently, so we have suppressed these warnings.
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Open up the file containing training data
xls=pd.ExcelFile('./t.xlsx')
training = pd.read_excel(xls)
del training['Content']

# Determine which pieces of data will be used for each theoretical construct
Clear=training[['Author', 'avg_word_sentence', 'num_misspelled', 
'bin_taboo', 'grammar_check', 'Subjectivity', 'Clear_l']].dropna()
Credible=training[[ 'Date', 'info _author', 'avg_word_sentence', 'num_misspelled', 
'bin_taboo', 'Polarity', 'Credible_l']].dropna()
Complete=training[['info _author','info_content','Average IDF', 'Entropy', 'Polarity',
       'Subjectivity', 'Complete_l']].dropna()
Correct=training[['info _author','Polarity', 'grammar_check', 'num_misspelled', 'Correct_l']].dropna()

# Perform some pre-processing on the data and separate out the 
# data that will be used in each training phase
X_Clear=Clear[Clear.columns.difference(['Clear_l'])].dropna()
Y_Clear=Clear['Clear_l'].dropna()
X_Credible=Credible[Credible.columns.difference(['Credible_l'])].dropna()
Y_Credible=Credible['Credible_l'].dropna()
X_Complete=Complete[Complete.columns.difference(['Complete_l'])].dropna()
Y_Complete=Complete['Complete_l'].dropna()
X_Correct=Correct[Correct.columns.difference(['Correct_l'])].dropna()
Y_Correct=Correct['Correct_l'].dropna()

# Just some diagnostic information to make sure things are running fine so far
print(Clear['Clear_l'].unique())
print(Complete['Complete_l'].unique())
print(Correct['Correct_l'].unique())
print(Credible['Credible_l'].unique())

def train_test(X,Y,test_size):
    """
    Appears to split the available data set into training and testing halves
    """
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state=25)
    return X_train, X_test, y_train, y_test

def fit_model(model,X_train, X_test, y_train, y_test):
    """
    Appears to perform some form of linear regression
    """
    ml_model = model
    result = ml_model.fit(X_train,y_train)
    prediction = result.predict(X_test)
    return prediction, result

def train_models():
    # In[97]:
    # Train the Clear model
    # The RandomForestRegressor cannot be reused for training
    # the different models! (I have tried)
    X_train, X_test, y_train, y_test = train_test(X_Clear,Y_Clear,test_size=0.3)
    prediction, clear_model = fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)

    # In[109]:
    # Train the Credibility model
    X_train, X_test, y_train, y_test = train_test(X_Credible,Y_Credible,test_size=0.3)
    prediction, credible_model = fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)

    # In[112]:
    # Train the completeness model
    X_train, X_test, y_train, y_test = train_test(X_Complete,Y_Complete,test_size=0.3)
    prediction, complete_model = fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)

    # In[116]:
    # Train the Correctness model
    X_train, X_test, y_train, y_test = train_test(X_Correct,Y_Correct,test_size=0.3)
    prediction, correct_model = fit_model(RandomForestRegressor(),X_train, X_test, y_train, y_test)

    return clear_model, credible_model, complete_model, correct_model


# Train models for all 4 constructs
clear_model, credible_model, complete_model, correct_model = train_models()



def test_func(X, Y, model, op, percentile=95):
    col=X.columns
    ntest=test[test.columns.difference(['Answers'])]
    ntest=pd.get_dummies(ntest)
    ntest=ntest[col]
    
    allTree_preds = np.stack([t.predict(ntest) for t in model.estimators_], axis = 0)
    
    err_down = np.percentile(allTree_preds, (100 - percentile) / 2.0  ,axis=0)
    err_up = np.percentile(allTree_preds, 100- (100 - percentile) / 2.0  ,axis=0)
    
    ci = err_up - err_down
    yhat = model.predict(ntest)
    # y = y_test
    
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

def calc_range(df,text):
    ma=max(df[text])
    mi=min(df[text])
    r = ma - mi
    correctedStartValue = df[text] - mi
    col=text+' %'
    df[col] = (correctedStartValue * 100) / r



def perform_regression(initial_data):
    # In[107]:
    # Perform regression with regards to clearness
    clear_data = test_func(X_Clear,'Clear_1', clear_model, initial_data)

    # In[111]:
    # Perform regression with regards to credibility
    cred_data = test_func(X_Credible,'Credible_1',credible_model,clear_data)

    # In[115]:
    # Perform regression with regards to completeness
    complete_data = test_func(X_Complete,'Complete_1',complete_model,cred_data)

    # In[117]:
    # Perform the final regression with regards to completeness
    final = test_func(X_Correct,'Correct_1',correct_model,complete_data)

    # In[120]:
    # Turn the numbers generated from regressions into 
    # human-understable percentages
    calc_range(final,'Correct_1')
    calc_range(final,'Complete_1')
    calc_range(final,'Credible_1')
    calc_range(final,'Clear_1')

    return final

def get_regression_scores(df):
    return {
        'clearness': df['Clear_1 %'][0],
        'credibility': df['Credible_1 %'][0],
        'completeness': df['Complete_1 %'][0],
        'correctness': df['Correct_1 %'][0]
    }


if __name__ == "__main__":
    # In[105]:
    # Read in test data
    test=pd.read_excel('./test.xlsx')

    final = perform_regression(test)
    scores = get_regression_scores(final)
    print(scores)

    # In[123]:
    # Output the final results of testing to an Excel file
    final.to_excel('./output.xlsx',index=False)