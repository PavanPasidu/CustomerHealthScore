# Get datasets 
import pandas as pd
import numpy as np
import warnings
import pickle
import os

from .Preprocessing.RecordAgreement import RecordAgreement
from .Preprocessing.RemoveOutliers import RemoveOutliers
from .Preprocessing.FillingMissingVlaues import FillingMissingValues
from .Preprocessing.Labeling import Labeling
from .Preprocessing.Encoder import Encoder
from .Preprocessing.CleanColumndata import Cleaner
from .Constant import Constant as const
from .Servicenow.GetServicenowData import GetServicenowData
from .Servicenow.UpdateTableServicenow import PutDataServicenow
from .Preprocessing.ConverttoCSV import ConverttoCSV
from .Merging.MergingDatasets import MergingDatasets
from .ModelTrain.ModelTraining import ModelTraining


class Train:
    def __init__(self):
        pass


    class LoadDatasets:
        def __init__(self):
            super().__init__()
        def getDatasets():
            warnings.filterwarnings('ignore')
            constant = const
            servicenow = GetServicenowData(const=constant, url='https://wso2sndev.service-now.com/oauth_token.do')
            csv = ConverttoCSV(constant=constant, servicenow=servicenow)

            filepath = 'E:/Research/Datasets/WSO2/Healthscore_dataset'       # Replace this path with path/to/NPSsurvey.csv
            nps = pd.read_csv(filepath + '/NPS.csv')

            caseData,accountData = csv.getData()
            return caseData,accountData,nps

    class Encoder:
        def __init__(self):
            super().__init__()
        def encode(nps):
            # Get encoded dataframe
            adj = Encoder(nps)
            temp_d2 = adj.adjustingDataset()
            encode = Encoder(temp_d2)
            encodedNPS = encode.customEncoder()
            return encodedNPS

    class Preprocessing:
        def __init__(self):
            super().__init__()

        def dropingDuplicates(temp_d3):
            duplicateSUM = temp_d3.duplicated().sum()
            if duplicateSUM != 0:
                temp_d3 = temp_d3.drop_duplicates()
            else: 
                None
            return temp_d3

        def getAgrrement(temp_d3):
            ''' 
            Here I am considering low agreement data records as outliers. Since I can not decide which record is the 
            outlier from multiple responses from single account, I am going to drop all the responses belongs to that account name.
            '''
            agreement = RecordAgreement(temp_d3)                             
            highAgreementdf = agreement.gethighAgreementSurveys()                    
            return highAgreementdf

        def removeOutliers(highAgreementdf):
            '''
            Here I am considering differnce between mode and other values of likely to recommend us as the removing criteria of outliers.
            '''
            temp_df1 = highAgreementdf
            outlierObj = RemoveOutliers(temp_df1)
            filtered_df = outlierObj.removeOutliers()
            return filtered_df

        def fillingMissingValues(filtered_df, caseDataset):
            temp_df2 = filtered_df
            fm = FillingMissingValues(temp_df2, caseDataset)
            filled_df, filledCaseDataset = fm.getFilledDataset()
            return filled_df, filledCaseDataset


        def labeling(filled_df):
            labeling = Labeling(filled_df)
            labeledDataset = labeling.returnLabeleddf()
            print("Labeled Dataset: \n", labeledDataset)
            return labeledDataset

    class Merger:
        def __init__(self):
            super().__init__()

        def mergeDataset(is_train, labeledDataset, caseData, accountData):
            # cleaner = Cleaner()
            # caseData = cleaner.cleanSyntaxPrefixes(df=caseData)
            merger = MergingDatasets(nps=labeledDataset, caseData=caseData, accountData=accountData, is_train=is_train)
            merged_dataset = merger.mergeDataset()
            merged_dataset.to_csv("E:/Research/CHS_Repo/CustomerHealthScoreB2B/Data/MergedDataset.csv")
            print("Merged Dataset\n",merged_dataset)
            return merged_dataset


    class Servicenow:
        def __init__(self):
            super.__init__()

        def pushData(df):
            tableName = 'u_customerhealthscoretraindata'
            url = "https://wso2sndev.service-now.com/api/wso2/customer_health/update_chs_table"
            sn = PutDataServicenow(table_name=tableName, instance_url=url, auth_url = 'https://wso2sndev.service-now.com/oauth_token.do')
            sn.push_dataframe_to_servicenow(df=df, const=const)

        def getData():
            pass

    class Model:
        def __init__(self):
            super().__init__()
        
        def trainModel(mergedDataset):
            # Train a model    ----merged_dataset----
            mergedDataset = pd.read_csv('E:/Research/CHS_Repo/CustomerHealthScoreB2B/Data/TrainingDataset/training.csv')
            modelObj = ModelTraining(mergedDataset)
            model,mse = modelObj.modelTrain()
            return model,mse

        def saveModel(model):
            filename = os.listdir('./Models/VersionNew')
            if len(filename) == 1:
                version = int(filename[0].split('_')[1])  + 1
                path = './Models/VersionNew/' + filename[0]
                os.remove(path)                                                                             # remove the existing file
            elif len(filename) == 0:
                version = 0
            else:print('There can not be more than 1 file in this directory')


            file_path_new = './Models/VersionNew/customerhealthscoremodel_' + str(version) + '_v' + '.pkl'    # save the new version
            with open(file_path_new, 'wb') as f:
                pickle.dump((model), f)
            file_path_old = './Models/VersionOld/customerhealthscoremodel_' + str(version) + '_v' + '.pkl'    # All the older versions reside here
            pickle.dump(model, open(file_path_old, 'wb'))


