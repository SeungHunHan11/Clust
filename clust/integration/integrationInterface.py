import sys
sys.path.append("../")
sys.path.append("../..")
sys.path.append("../../..")
    
from Clust.clust.integration.ML import RNNAEAlignment
from Clust.clust.integration.meta import data_integration


class IntegrationInterface():
    """
    Data Integration Class
    """
    def __init__(self):
        pass
        
    def multipleDatasetsIntegration(self, integration_param, multiple_dataset):
        """ 
        dataSet과 Parameter에 따라 데이터를 병합하는 함수

         1. 각 데이터셋에서 병합에 필요한 partial_data_info (각 컬럼들에 대한 특성) 추출
         2. 명확하게 정합 주기 값이 입력 없을 경우 최소공배수 주기를 설정함
         3. 각 데이터들에 대한 Preprocessing  
         4. 입력 method에 따라 3가지 방법 중 하나를 선택하여 정합함

        Args:
            integration_param (dictionary) : Integration을 위한 method, transformParam이 담긴 Parameter
            multiple_dataset (dictionary)
            
        Returns:
            DataFrame : integrated_data

        Example:
            >>> re_frequency_min = 3
            >>> timedelta_frequency_min = datetime.timedelta(minutes= re_frequency_min)

            >>> integration_param   = {
            ...    "integration_duration_type":"common",
            ...    "integration_frequency":timedelta_frequency_min,
            ...    "param":{},
            ...    "method":"meta"}
        """ 
        for i, df_name in enumerate(multiple_dataset):
            multiple_dataset[df_name] = multiple_dataset[df_name].add_suffix('_'+str(i))
            
        integrationMethod = integration_param['method']
        integration_freq_min    = integration_param["integration_frequency"]
        integration_duration_type    = integration_param["integration_duration_type"]
        
        from Clust.clust.integration.meta import partialDataInfo
        partial_data_info = partialDataInfo.PartialData(multiple_dataset, integration_duration_type)
        overlap_duration = partial_data_info.column_meta["overlap_duration"]
        ## Integration
        imputed_datas = {}
        
        
        print("===integrationStart===")
        for key in multiple_dataset.keys():
            imputed_datas[key]=(multiple_dataset[key])
        if integrationMethod=="meta":
            integrated_data = self.getIntegratedDataSetByMeta(imputed_datas, integration_freq_min, partial_data_info)
        elif integrationMethod=="ML":
            integrated_data = self.getIntegratedDataSetByML(imputed_datas, integration_param['param'], overlap_duration)
        elif integrationMethod=="simple":
            integrated_data = self.IntegratedDataSetBySimple(imputed_datas, integration_freq_min, overlap_duration)
        else:
            integrated_data = self.IntegratedDataSetBySimple(imputed_datas, integration_freq_min, overlap_duration)
        print("===integrationEnd===")
       

        return integrated_data

    def getIntegratedDataSetByML(self, data_set, transform_param, overlap_duration):
        """ 
        ML을 활용한 데이터 병합 함수
        1. 병합한 데이터에 RNN_AE 를 활용해 변환된 데이터를 반환

        Args:
            data_set (json): 병합하고 싶은 데이터들의 셋
            transform_param (json): RNN_AE를 하기 위한 Parameter
            overlap_duration (json): 병합하고 싶은 데이터들의 공통 시간 구간
        
        Returns:
            DataFrame: integrated_data by transform

        Example:
            >>> overlap_duration = {'start_time': Timestamp('2018-01-03 00:00:00'), 
            ...                     'end_time': Timestamp('2018-01-05 00:00:00')}
        """
        
        ## simple integration
        data_int = data_integration.DataIntegration(data_set)
        dintegrated_data = data_int.simple_integration(overlap_duration)
        
        model = transform_param["model"]
        transfomrParam = transform_param['param']
        if model == "RNN_AE":
            integratedDataSet = RNNAEAlignment.RNN_AE(dintegrated_data, transfomrParam)
        else :
            print('Not Available')
            integratedDataSet= None
            
        return integratedDataSet

    def getIntegratedDataSetByMeta(self, data_set, integration_freq_min, partial_data_info):
        """ 
        Meta(column characteristics)을 활용한 데이터 병합 함수

        Args:
            data_set (json): 병합하고 싶은 데이터들의 셋
            integration_freq_min (json): 조정하고 싶은 second 단위의 Frequency
            partial_data_info (json): column characteristics의 info
            
        Returns:
            DataFrame: integrated_data   
        """
        ## Integration
        data_it = data_integration.DataIntegration(data_set)

        integratedDataSet = data_it.dataIntegrationByMeta(integration_freq_min, partial_data_info.column_meta)
        
        return integratedDataSet 
    
    def IntegratedDataSetBySimple(self, data_set, integration_freq_min, overlap_duration):
        """ 
        Simple한 병합

        Args:
            data_set (json): 병합하고 싶은 데이터들의 셋
            integration_freq_min (json): 조정하고 싶은 second 단위의 Frequency
            overlap_duration (json): 조정하고 싶은 second 단위의 Frequency
            
        Returns:
            DataFrame: integrated_data
        """
        ## simple integration
        #re_frequency = datetime.timedelta(seconds= integration_freq_sec)
        data_int = data_integration.DataIntegration(data_set)
        integratedDataSet = data_int.simple_integration(overlap_duration)
        integratedDataSet = integratedDataSet.resample(integration_freq_min).mean()
        
        return integratedDataSet





