## Generate a Cover Letter for Your Resume (FastApi)

- This is a simple python script that generates a cover letter for your resume.

> Requirement
- Python 3.7 or above
- LibreOffice installed on your computer


> Setup the Application
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> Run the program
```bash
python main.py
```
> Remove unwanted files
```bash
pyclean -v . # Remove unwanted files
```

## Note:- If libreoffice is not installed on your computer, run the following command
```bash
sudo apt-get install -y libreoffice libreoffice-writer
sudo apt-get install -y unoconv
sudo sed -i "s|#!/usr/bin/env python3|#!/usr/bin/python3 |g" /usr/bin/unoconv
```

## Note:- Local application into public url using localtunnel
> Check if npm is installed
```bash
npm -v
```
> If not installed, install npm
```bash
sudo apt install npm
```
> Install localtunnel
```bash
npm install -g localtunnel
```
> Run the application
```bash
python main.py
```
> Run localtunnel
```bash
lt --port 9000 --subdomain <subdomain> # e.g lt --port 9000 --subdomain coverLetter
```
- where 9000 is the port number of the application
- where <subdomain> is the subdomain of the application