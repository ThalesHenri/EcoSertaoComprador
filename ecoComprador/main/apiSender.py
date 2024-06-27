#this is a class that will hand sending the information for the form to an api
#made by tEaGaH
import requests
class ApiSender:
    def __init__(self,url):
        self.url = url
        self.formData = {}
        
    def addFormData(self,key,value):
        self.formData[key] = value
        
    def sendPostRequest():
        response = requests.post(self.url, data=self.form_data)
        
        if response.status_code == 200:
            print("Form data submitted successfully.")
            try:
                print("Response:", response.json())
            except ValueError:
                print("Response:", response.text)
        else:
            print("Failed to submit form data.")
            print("Status code:", response.status_code)
            print("Response:", response.text)

    
