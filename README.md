# flask_technical_test
Technical test of a REST API for an Hospital 

## what was achieved?

This API allows you do the following:

**1**. create user of 3 types: Patient, Hospital and Doctor. The last can only be created by the former.<br>
**2**. Email confirmation. without confirmation users cannot log in.<br>
**3**. Only doctor can create medical records for patient users. can create as many as he want for the same user. This was intended for be able to have the medical history of a patient, thats the reason why i added date to the records.<br>
**4**. The first time the doctor Log in have to change the password.<br>

Requests to this API were tested using Insomnia. There, data in POST request was given as JSON format and actions, like create a doctor user, were authorized through a TOKEN given in the headers. 

This app was done with flask and postgres data base. the lastone was deployed on heroku and the link is exposed in the code. 

## how to test it?

* clone this repository <br>
``` git clone https://github.com/juanjo255/flask_technical_test.git ```
* install requeriments <br>
``` pip install -r requirements.txt ```
* run app <br>
```flask run```
