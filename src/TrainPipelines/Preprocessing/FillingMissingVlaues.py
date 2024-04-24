import pandas as pd
import pickle

class FillingMissingValues:
    def __init__(self,df,caseDf):
        self.df =  df
        self.caseDf = caseDf

    # Filling missing values of encoded_product_impact,encoded_responsiveness,encoded_satisfaction with mode,median
    # function to fill missing values with mode, excluding multiple modes
    def fill_missing(self,group):
        for col in group[['encoded_satisfaction', 'encoded_responsiveness',
        'encoded_product_impact']].columns:  
            mode_values = group[col].mode()
            median_values = group[col].median()
            
            if len(mode_values) == 1:                               # Only fill if there's a single mode
                group[col] = group[col].fillna(mode_values[0])
            elif len(mode_values)==2 and col!='encoded_product_impact':
                group[col] = group[col].fillna(mode_values.mean())
            elif len(mode_values)>=3 and col!='encoded_product_impact':
                group[col] = group[col].fillna(mode_values.median())
            else:
                if col!='encoded_product_impact':
                    group[col] = group[col].fillna(median_values)   
        return group


    def fill_missing_fcr(self):
        filename = 'E:/Research/CHS_Repo/CustomerHealthScoreB2B/Models/Imputation_Model/fcrimputationModel.pkl'
        model = pickle.load(open(filename, 'rb'))
        temp_df = self.caseDf.copy()

        def custom_encode(boolean_value):
            if pd.isnull(boolean_value):
                return boolean_value
            else:
                return 1 if boolean_value else 0
        temp_df['First Contact Resolution'] = temp_df['First Contact Resolution'].map(custom_encode)


        X_missing = temp_df[temp_df['First Contact Resolution'].isnull()][['Time To Resolve']]
        predicted_values = model.predict(X_missing)

        filledcaseDataset = temp_df.drop(['Unnamed: 0'],axis=1).copy()
        filledcaseDataset.loc[filledcaseDataset['First Contact Resolution'].isnull(), 'First Contact Resolution'] = predicted_values
        filledcaseDataset = filledcaseDataset.dropna(subset=['Account'])


    # Apply the function to each group
    def getFilledDataset(self):
        filledCaseDataset = pd.DataFrame()#self.fill_missing_fcr()
        filled_df = self.df.groupby('Account Name').apply(self.fill_missing).reset_index(drop=True)
        filled_df = filled_df.fillna(-1)
        return filled_df,filledCaseDataset