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

## Output

Console:
```

C:\Users\18589\Dropbox\AWS\aws-document-lambda-configurations>Scripts\activate

(aws-document-lambda-configurations) C:\Users\18589\Dropbox\AWS\aws-document-lambda-configurations>python document_lambdas.py
Getting lambda data ...
Getting lambda event sources ...
Getting S3 sources ...
BingSpellcheck                          <-
BlogBuild                               <-
aws-code-index-bulk-load                <- arn:aws:sqs:us-east-1:xxx:code-index
aws-code-index-escape-files             <- s3:code-index-3
aws-code-index-format-files             <- s3:code-index-3
aws-code-index-stream-bulk-load         <- arn:aws:dynamodb:us-east-1:xxx:table/code-index/stream/2018-12-16T17:13:15.772
```

lambda_data.csv:
