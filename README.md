## About
This directory contains a practice of text detection using Google Cloud Vison API based on https://cloud.google.com/vision/docs/fulltext-annotations.

## Setup
```
$ pip install -r requirements.txt
```

## Run
1. Authentication: running locally Google Cloud SDK
```
$ gcloud auth application-default login
```
The browser will open the new window to verify the account.
2. Activate Virtualenv
```
$ Source env/bin/activate
```
3. Run doxtext.py
```
$ python doctext.py orc.jpg -out_file out.jpg
```
4. Result:
![ocr](https://user-images.githubusercontent.com/12990822/27521140-e1bbc148-59de-11e7-9b2c-187b862deee1.jpg)
![out](https://user-images.githubusercontent.com/12990822/27521144-f1f761fc-59de-11e7-9c59-4ed7f924da84.jpg)

