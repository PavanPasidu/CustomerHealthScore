'''
Here I am using trained model and predict the healthscore.And 
also I will get sentiment value through an API and combine it
with healthscore. Combining sentiment to healthscore will be 
done dailybasis.

'''
import pandas as pd
import pickle
import warnings
import sys
import os

sys.path.append("..")
from ..TrainPipelines.train import Train
from .Database.database import Database

class Predictor:
   def __init__(self):
      pass
    
   def loadModel(self):
      filename = os.listdir('./Models/VersionNew')[0]
      filepath = f'./Models/VersionNew/{filename}'
      load_model = pickle.load(open(filepath, 'rb')) 
      return load_model

   def preprocess(self):
      trainer = Train()
      caseData,accountData,nps = trainer.LoadDatasets.getDatasets()
      encodedNPS = trainer.Encoder.encode(nps=nps)
      noduplicateDF = trainer.Preprocessing.dropingDuplicates(encodedNPS)
      highConcensusDF = trainer.Preprocessing.getAgrrement(noduplicateDF)  #####
      noOutliersDF = trainer.Preprocessing.removeOutliers(highConcensusDF) #####
      filledNPS,_ = trainer.Preprocessing.fillingMissingValues(noOutliersDF, caseData)
      mergedDF = trainer.Merger.mergeDataset(False, filledNPS, caseData, accountData)
      return mergedDF

   def predict(self):
      model = self.loadModel()
      merged_dataframe = self.preprocess()
      tempmergedDf = pd.read_csv('E:/Research/CHS_Repo/CustomerHealthScoreB2B/Data/inferencing.csv')

      X_test = tempmergedDf.drop(['AccountName','healthScore'],axis=1)
      y_pred = model.predict(X_test) 
      df = tempmergedDf[['AccountName']]
      df['HealthScore'] = y_pred

      # Save the dataset in Servicenow/MySQL database
      dbhandler = Database(df=df)
      dbhandler.insertdb()

'''Healthscore will change according to sentiment coming from sentiment model (throughout the 6 months).
   Once in six month healthscore will be overridden by runing this pipeline   
'''