import requests

class Patient:

    def __init__(self):
        self.data = [] 
        self.processed_data_to_send_to_azure = {
            "Inputs": {
                "data" : [{}]
            },
            "GlobalParameters": {
                "method": "predict_proba"
            }
        }
        self.raw_azure_prediction = {}
        self.URL = "http://cd8f5b31-36f5-40dd-9adc-47d327a37a9f.southcentralus.azurecontainer.io/score"
        self.CLASSES = ["Asthma", "Bronchiectasis", "Bronchiolitis", "COPD", "Healthy", "LRTI", "Pneumonia", "URTI"]

    def post_data_to_azure(self, data):
        self.data = data
        for i in range(100):
            self.processed_data_to_send_to_azure["Inputs"]["data"][0][f"Feature {i+1}"] = data[i]
        resp = requests.post(self.URL, json=self.processed_data_to_send_to_azure)
        
        return_dict = {}
        for i in range(len(self.CLASSES)):

            return_dict[self.CLASSES[i]] = round(resp.json()["Results"][0][i]*100,2)

        return return_dict

    def post_data_to_azure_testing(self, data):
        self.data = data
        for i in range(100):
            self.processed_data_to_send_to_azure["Inputs"]["data"][0][f"Feature {i+1}"] = data[i]
        resp1 = requests.post(self.URL, json=self.processed_data_to_send_to_azure)
        
        self.processed_data_to_send_to_azure["GlobalParameters"]["method"] = "predict"
        resp2 = requests.post(self.URL, json=self.processed_data_to_send_to_azure)
        
        return resp1, resp2
