from .train import Train

class Runner:
    def __init__(self):
        self.trainer = Train()

    def getCurrentMSE(self,new_mse):
        constant = 100
        with open('./Models/current_mse.txt','+r') as file:
            exist = len(file.read(1))

            if exist<1:
                file.write(str(new_mse))
                return new_mse*constant
            else:
                file.seek(0)
                current_mse = float(file.read())
                return current_mse
            
            
    def saveModel(self,model,mse):
        trainer = self.trainer
        current_mse = self.getCurrentMSE(mse)
        print('Current M.S.E. : ',current_mse)
        if mse<current_mse:
            trainer.Model.saveModel(model)
            with open('./Models/current_mse.txt','+w') as file:
                file.write(str(mse))
        else:pass



    def run(self):
        trainer = self.trainer
        caseData,accountData,nps = trainer.LoadDatasets.getDatasets()
        encodedNPS = trainer.Encoder.encode(nps=nps)

        noduplicateDF = trainer.Preprocessing.dropingDuplicates(encodedNPS)
        highConcensusDF = trainer.Preprocessing.getAgrrement(noduplicateDF)
        noOutliersDF = trainer.Preprocessing.removeOutliers(highConcensusDF)
        filledNPS,filledCases = trainer.Preprocessing.fillingMissingValues(noOutliersDF,caseData)
        labeledDF = trainer.Preprocessing.labeling(filledNPS)

        mergedDF = trainer.Merger.mergeDataset(True,labeledDF,caseData,accountData)

        model,mse = trainer.Model.trainModel(mergedDF)
        self.saveModel(model=model,mse=mse)
