## Automating Lead Generation and Email Outreach

This program will scrap the business details like Name, Address, Website, Phone No., Email ID of various businesses from google maps and generate email text messages using OpenAI API. Along with this, it will send the email to the respective business using their Email ID.

### Steps to run the program:
1. Clone this repository:
```
git clone https://github.com/mohitnilkute013/Automating-Lead-Generation-and-Email-Outreach.git
```

2. Create virtual environment:
```
conda create -p venv python=3.8
```

3. Install the dependencies:
```
pip install -r requirements.txt
```

4. Run the main.py file:
```
python main.py
```


For testing purposes, I have used my mail id so it will send the mails to my email id. You can change the line according to your choice:
```
Email = "mohitnilkute012@gmail.com"
```
<br>

Make sure to `put your credentials` in your `credentials folder!!!`
#### You will have to edit 2 files!

1. `gsheet.json`
It's Structure looks like:
```
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": "",
  "universe_domain": ""
}
```
Make sure to put your Google sheets json key here.
Also, Make sure the Google Sheets API and Google Drive API is Enabled on website: 
```
https://console.cloud.google.com/projectselector2/apis/dashboard?pli=1&supportedpurview=project&authuser=1
```


2. `.env`
This is a environment file. It contains the following environment variables:
```
OPENAI_API_KEY="your_openai_api_key"
EMAIL="your_mail_id"
PASSWORD="your_mail_id_password"
```

Make sure to replace your OPENAI_API_KEY, EMAIL and PASSWORD.
This is required to login into your Gmail Account for sending emails. And, also for connecting OpenAI API.

`Note`: For now, the OpenAI account does not have a free subscription. So, I have not tested upon the OpenAi API. but according to my knowledge, it should work fine. If any problem occurs, make sure to check the logs.