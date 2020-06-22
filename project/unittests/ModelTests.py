#!/usr/bin/env python
"""
model tests
"""


import unittest

## import model specific functions and variables
from model import *

class ModelTest(unittest.TestCase):
    """
    test the essential functionality
    """
    data_dir = "../data/cs-train"
        
    def test_01_train(self):
        """
        test the train functionality
        """

        ## train the model
        model_train(ModelTest.data_dir,test=True)
        models = [f for f in os.listdir(os.path.join("..", "models")) if re.search("test", f)]
        self.assertEqual(2,len(models))

    def test_02_load(self):
        """
        test the train functionality
        """
                        
        ## load the model
        _,models = model_load(data_dir=ModelTest.data_dir,test=True)
        
        self.assertEqual(2,len(models))
       
    def test_03_predict(self):
        """
        test the predict function input
        """
        data, models = model_load(data_dir=ModelTest.data_dir, test=True)
        ## test predict
        country = 'all'
        year = '2018'
        month = '01'
        day = '05'
        result = model_predict(country, year, month, day, all_models=models,all_data=data, test=True)
        self.assertTrue("y_prob" in result)
        self.assertTrue("y_proba" in result)
        print(result)

          
### Run the tests
if __name__ == '__main__':
    unittest.main()
