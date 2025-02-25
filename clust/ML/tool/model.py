import sys, os
sys.path.append("../")
sys.path.append("../../")
sys.path.append("../../../")

from Clust.clust.ML.common import model_path_setting
import pickle

def get_model_path(train_data_path_list, method):
    """ get fullModelFilePath
    Ths function makes fullModelFilePath list.
    trainDataPathList and other paths obtained by method can be used for creating fullModelFilePath.

    :param trainDataPathList: It includes train data information to generate model path
    :type trainDataPathList: list of str

    :param method: train method
    :type method: str

    Example:

        >>>  trainDataPathList =['DBName', 'MSName', 'columnName' ]
        >>>  trainMethod ='brits'
        >>>  modelFilePath = MI.getModelFilePath(trainDataPathList, self.trainMethod)
    """ 
    model_info_list = model_path_setting.my_model_info_list
    model_info = model_info_list[method]
    
    model_full_path =model_info['model_root_path']+model_info['model_info_path']+train_data_path_list
    model_folder_path=''
    for add_folder in model_full_path:
        model_folder_path = os.path.join(model_folder_path, add_folder)

    if not os.path.exists(model_folder_path):
        os.makedirs(model_folder_path)
    
    model_file_path=[]
    for i, model_name in enumerate(model_info['model_file_names']):
        model_file_path.append(os.path.join(model_folder_path, model_name))
    return model_file_path


# get model path
def get_model_file_path(train_data_path_list, model_method):
    model_file_path_list = get_model_path(train_data_path_list, model_method)
    model_file_path = ''.join(model_file_path_list)
    print(model_file_path)

    return model_file_path


## Pickle
def save_pickle_model(model, model_file_path):
    """ save model: dafult file type is pickle
    
    Args:
        model_file_path(str) : model_file_path
    
    """
    with open(model_file_path, 'wb') as outfile:
        pickle.dump(model, outfile)


def load_pickle_model(model_file_path):
    """ 
    load model: : dafult file type is pickle

    Args:
        model_file_path(str) : model_file_path
    
    """
    with open(model_file_path, 'rb') as infile:
        model = pickle.load(infile)

    return model
