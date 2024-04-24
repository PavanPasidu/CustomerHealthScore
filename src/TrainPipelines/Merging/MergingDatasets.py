import pandas as pd


class MergingDatasets:
    tables = list()
    def __init__(self,nps,caseData,accountData,is_train=True):
        self.caseData    =   caseData
        self.accountData =   accountData
        self.nps         =   nps
        self.is_train    =   is_train

    def mergeDataset(self,start='2022-02-01',end='2022-08-01'):
        filtered_df     =   self.getChunkofData(df=self.caseData,start=start,end=end)

        def getFCRpercantage(col):
            true_count  = col.sum()
            total_count = len(col)
            percentage_true = (true_count / total_count) * 100
            return percentage_true

        # Convert data to numeric
        filtered_df[["agent_reassignment_count", "time_to_resolve","reopen_count","is_fcr"]] = filtered_df[["agent_reassignment_count", "time_to_resolve","reopen_count","is_fcr"]].apply(pd.to_numeric)

        grouped_data    = filtered_df.groupby('account_name').agg({
            'agent_reassignment_count': 'mean', 
            'time_to_resolve': 'mean',
            'reopen_count': 'mean',
            'is_fcr': getFCRpercantage, 
        })
        self.tables.append(grouped_data.reset_index())
        concat_data = self.concatanateData(tables=self.tables)
        return concat_data


    def getChunkofData(self,df,start='2022-02-01',end='2022-08-01'):
        df['sys_created_on'] = pd.to_datetime(df['sys_created_on'], format='%Y-%m-%d %H:%M:%S')

        start_date  = pd.to_datetime(start)
        end_date    = pd.to_datetime(end)

        filtered_df = df[(df['sys_created_on'] >= start_date) & (df['sys_created_on'] <= end_date)]
        return filtered_df
    

    def concatanateData(self,tables):
        concatenated_df = pd.concat(tables, ignore_index=True)
        if self.is_train:
            concat_data   = pd.merge(concatenated_df, self.nps[['Account Name','Sales Region','Sub Region','healthScore']], left_on='account_name', right_on='Account Name', how='left')
        else:
            concat_data   = pd.merge(concatenated_df, self.nps[['Account Name','Sales Region','Sub Region']], left_on='account_name', right_on='Account Name', how='left')
        header_map = {"Account Name":"AccountName"}
        concat_data.rename(columns=header_map,inplace=True)
        return concat_data
        
    

