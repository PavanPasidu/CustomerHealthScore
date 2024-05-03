from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.utils import shuffle
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso,BayesianRidge                     
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from sklearn.svm import SVR
import warnings


class ModelTraining:
    # Split the dataset
    X,y = None, None
    X_train = X_test = y_train =  y_test = None

    def __init__(self,df):
        self.df = df


    def modelSelection(self):
        global X,y,X_train, X_test, y_train, y_test

        X = self.df.drop(['healthScore','AccountName'],axis=1)
        y = self.df[['healthScore']]

        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        models = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(),
            'Lasso Regression': Lasso(),
            'SVR': SVR(),
            'Random Forest Regressor': RandomForestRegressor(),
            'Gradient Boosting Regressor': GradientBoostingRegressor(),
            'XGBRegressor': xgb.XGBRFRegressor(objective ='reg:squarederror'),
            'Baysian Regressor':BayesianRidge()
        }

        mse_values        = dict()
        lowest_mse        = 20000
        lowest_mse_model  = None
        best_model_name   = 'Linear Regression'
        for model_name, model in models.items():
            model.fit(X_train, y_train)
            warnings.filterwarnings('ignore')
            y_pred = model.predict(X_test)

            mse = mean_squared_error(y_test, y_pred)
            mse_values[model_name]      =  [mse,model]
            if mse<lowest_mse:
                lowest_mse              =  mse
                lowest_mse_model        =  model
                best_model_name         =  model_name
            else:continue
        
        tunedParams =   self.hyperParameterTuning(lowest_mse_model,best_model_name)

        return lowest_mse_model,best_model_name,tunedParams


    def hyperParameterTuning(self,model,best_model_name):
        global X_train, y_train

        param_grid = {}

        if best_model_name == "Linear Regression":
            param_grid = {
                
            }
        elif best_model_name == "Ridge Regression":
            param_grid = {
                'alpha': [0.01, 0.1, 1.0, 10.0]
            }
        elif best_model_name == "Lasso Regression":
            param_grid = {
                'alpha': [0.01, 0.1, 1.0, 10.0]
            }
        elif best_model_name == "Baysian Regressor":
            param_grid = {
                'alpha_1': [1e-6, 1e-5, 1e-4],
                'alpha_2': [1e-6, 1e-5, 1e-4],
                'lambda_1': [1e-6, 1e-5, 1e-4],
                'lambda_2': [1e-6, 1e-5, 1e-4],
            }
        elif best_model_name == "Random Forest Regressor":
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        elif best_model_name == "Gradient Boosting Regressor":
            param_grid = {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7]
            }
        elif best_model_name == "XGBRegressor":
            param_grid = {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'gamma': [0, 0.1, 0.2]
            }
        elif best_model_name == "SVR":
            param_grid = {
                'C': [0.1, 1, 10],
                'kernel': ['linear', 'poly', 'rbf','sigmoid']
            }


        grid_search = GridSearchCV(model, param_grid, scoring='neg_mean_squared_error', cv=5)
        grid_search.fit(X_train, y_train)

        bestParams  = grid_search.best_params_
        return bestParams


    def modelTrain(self):
        global X_train, y_train

        bestModel,modelName,tunedParams   =   self.modelSelection()       # Get the best model,tuned Parameters

        # Choose the model
        best_model_with_tunedParams=None
        if modelName == "Linear Regression":
            best_model_with_tunedParams = LinearRegression(**tunedParams)
        elif modelName == "Ridge Regression":
            best_model_with_tunedParams = Ridge(**tunedParams)
        elif modelName == "Lasso Regression":
            best_model_with_tunedParams = Lasso(**tunedParams)
        elif modelName == "Baysian Regressor":
            best_model_with_tunedParams = BayesianRidge(**tunedParams)
        elif modelName == "Random Forest Regressor":
            best_model_with_tunedParams = RandomForestRegressor(**tunedParams)
        elif modelName == "Gradient Boosting Regressor":
            best_model_with_tunedParams = GradientBoostingRegressor(**tunedParams)
        elif modelName == "XGBRegressor":
            best_model_with_tunedParams = xgb.XGBRegressor(**tunedParams)
        elif modelName == "SVR":
            best_model_with_tunedParams = SVR(**tunedParams)

        # Train the model using the entire dataset
        best_model_with_tunedParams.fit(X_train, y_train)
        y_pred = best_model_with_tunedParams.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print('M.S.E. of the new model: ',mse)
        print('Model: ',modelName, "\nBest Params: ",tunedParams)
        return best_model_with_tunedParams,mse
