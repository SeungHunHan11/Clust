import numpy as np
import pandas as pd
  
class SerialImputation():
    """ This class applies a number of imputation techniques in series.
    """
    def __init__ (self):
        """ Define Imputation Methods
        """
        self.ScikitLearnMethods =['KNN','MICE']
        self.simpleMethods =['most_frequent', 'mean', 'median', 'constant']
        self.fillNAMethods = ['bfill','ffill']
        self.simpleIntMethods= ['linear', 'time', 'nearest', 'zero', 'slinear','quadratic', 'cubic', 'barycentric']
        self.orderIntMethods = [ 'polynomial', 'spline']
        #self.deepMethods = ['brits']
 
    def get_dataWithSerialImputationMethods(self, data, imputation_param):
        """ This function cleans the data by applying several missing data handling methods. 

        Args:
            data (DataFrame): input data
            imputation_param (json): parameter of imputation
            
        Returns:
            DataFrame: NewDataframe output
        
        Example:

            >>> imputation_param = {'flag': True, 
            ...                     'imputation_method': [{'min': 0, 'max': 3, 'method': 'KNN', 'parameter': {}},
            ...                                          {'min': 4, 'max': 6, 'method': 'mean', 'parameter': {}}],
            ...                     'total_non_NaN_ratio': 80}
            >>> output = SerialImputation().get_dataWithSerialImputationMethods(data, imputation_param)

        """
        result = data.copy()
        imputation_method = imputation_param['imputation_method']
        total_non_NaN_ratio = imputation_param['total_non_NaN_ratio']

        # if total column NaN number is less tan limit, Impute it according to the parameter  
        result = self.dropOverNaNThresh(result, total_non_NaN_ratio)
        
        if not result.empty:
            result = self.dfImputation(result, imputation_method)
        else:
            result =data.copy()
        
        for column in data.columns:
            if column in result.columns:
                data.loc[:, column] = result[column]
        return data

    def dropOverNaNThresh(self, data, total_non_NaN_ratio):
        """ This function removes any column that does not meet the qualifications (total Non-Nan Ratio).

        Args:
            data (DataFrame): input data
            total_non_NaN_ratio (float): total NaN Ratio
            
        Note
        ---------
        If the ratio of non-NaN values is less than or equal to the Ratio value, column data is removed.
            
            
        Returns:
            DataFrame: NewDataframe excluding columns that do not meet the qualifications
        
        Example:

            >>> total_non_NaN_ratio = 80 # %
            >>> output = SerialImputation().dropOverNaNThresh(data, imputation_param)

        """
        totalNonNanNum = int(total_non_NaN_ratio/100 * len(data)) 
        result= data.dropna(thresh = totalNonNanNum, axis=1)
       
        return result

    def printNaNDataSummary(self, data):
        """ Print Summary of data NaN status 

        Args:
            data (DataFrame): input data
        
        Example:

            >>> output = SerialImputation().printNaNDataSummary(data)

        """
        nan_data_summary = round(data.isna().sum()/len(data), 2)
        #print("===== NaN data Ratio summary ======")
        #print(nan_data_summary)


    def dfImputation(self, data, imputation_method):
        """ This function returns final imputed data after imputation and filtering by max NaN limit.

        Args:
            data (DataFrame): input data
            imputation_param (json): imputation_method
            
        Returns:
            DataFrame: NewDataframe after imputation and nan limit masking
        
        Example:

            >>> output = SerialImputation().dfImputation(data, imputation_param)
        """
        
        #self.printNaNDataSummary(data)
        DataWithMaskedNaN = data.copy()
        for method_set in imputation_method:
            max_limit =method_set['max']
            from Clust.clust.preprocessing.imputation import nanMasking
            NaNInfoOverThresh= nanMasking.getConsecutiveNaNInfoOvermaxNaNNumLimit(data, max_limit)
            # Missing Data Imputation
            
            data = self.imputeDataByMethod(method_set, data)
            DataWithMaskedNaN = nanMasking.setNaNSpecificDuration(data, NaNInfoOverThresh, max_limit)
        self.printNaNDataSummary(DataWithMaskedNaN)
        return DataWithMaskedNaN

    def imputeDataByMethod(self, method_set, data):
        """ This function imputes data depending on method_set. (min, max, method, method_parameter)

        Args:
            method_set (json): method information
            data (DataFrame): input data
            
        Returns:
            DataFrame: NewDataframe after imputation
        
        Example:

            >>> method_set = {'min': 0, 'max': 3, 'method': 'KNN', 'parameter': {}}
            >>> output = SerialImputation().imputeDataByMethod(method_set, data,)

        """
        
        min_limit = method_set['min']
        max_limit = method_set['max']
        method = method_set['method']
        parameter = method_set['parameter']

        from Clust.clust.preprocessing.imputation import basicMethod 
        from Clust.clust.preprocessing.imputation import DLMethod 
        basicImpute = basicMethod.BasicImputation(data, method, max_limit, parameter)
        
        if method in self.ScikitLearnMethods:
            result = basicImpute.ScikitLearnMethod()       
        elif method in self.simpleMethods:
            result = basicImpute.simpleMethod()
        elif method in self.simpleIntMethods:
            result = basicImpute.simpleIntMethod()
        elif method in self.fillNAMethods:
            result = basicImpute.fillNAMethod()
        elif method in self.orderIntMethods:
            result = basicImpute.orderIntMethod()
        elif method in self.deepMethods:
            result = DLMethod.DLImputation(data, method, parameter).getResult()
        else:
            result = data.copy()
            print("Couldn't find a proper imputation method.")

        return result        


