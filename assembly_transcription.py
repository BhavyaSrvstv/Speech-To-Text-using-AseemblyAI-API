import requests
from assembly_api import ASSEMBLY_API_KEY
import json

base_url="https://api.assemblyai.com/v2"
headers = {
    "authorization": ASSEMBLY_API_KEY 
}
#upload
def upload(filename):
  with open(filename,"rb") as f:
    response=requests.post(base_url+"/upload",
                       headers=headers,
                       data=f)

    upload_url=response.json()["upload_url"]
    return upload_url#this will return the url to where the file is uploaded
#transcribe
def transcribe(filename):
  data = {"audio_url": upload(filename)}
  url= base_url+"/transcript"
  response=requests.post(url,json=data,headers=headers)
  job_id=response.json()['id']
  return job_id#this will return id of the job of transcripting the uploaded file
#we will use this id to ask assembly ai if the job of trancripting the file completed or is still processing

#poll
def poll(filename):#we constantly poll the assembly api to  ask if the transcription is completed or not
   j_id=transcribe(filename)
   polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{j_id}"
   while True:
     transcription_result = requests.get(polling_endpoint, headers=headers).json()#we make a "get" request here because we are asking data from the endpoint
     # we make a "post" request when we have to send data to the endpoint
     if transcription_result['status'] == 'completed':
        return transcription_result #if the status is completed then return the result

     elif transcription_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {transcription_result['error']}")#or if there is error then raise a runtime error and print the error that has occureed
     
def output_file(filename,output_file):
  data=poll(filename) 

  text_filename=output_file+".txt"#we convert the data into a text file
  with open(text_filename,"w") as f:#open the file and write in it
    f.write(data['text'])#extracting text from the data
  print("Transcription saved!!")