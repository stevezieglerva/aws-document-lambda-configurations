# aws-document-lambda-configurations
Python script to gather information, including input events, for an account's AWS Lambda functions. This information is not available from a single API call. The script calls the necessary APIs and merges the results into a detailed CSV and simplified std output.

When looking to clean up and remove uncessary, redudant, and similar Lambdas, seeing all of the Lamba information, especially the input events, is very helpful.

## Installation
```python
pip install -r requirements.txt
```

## Execution
```python
python document_lambdas.py
```



