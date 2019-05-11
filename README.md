# aws-document-lambda-configurations
Python script to gather information, including input events, for an account's AWS Lambda functions. This information is not available from a single API call. The script calls the necessary APIs and merges the results into a detailed CSV and simplified std output.

When looking to clean up and remove uncessary, redudant, and similar Lambdas, seeing all of the Lamba information, especially the input events, is very helpful.

## Prerequisites and Installation
You need to have valid credentials for connecting to AWS services. The easiest way to do this is using the AWS CLI and set up your default credentials. If you can run a basic CLI command like the following, this script should work.

```bash
aws lambda list-functions

FUNCTIONS       EsWTYS1B8vqM=    3678         arn:aws:lambda:us-east-1:1175:function:aws-lnkchk-start aws-lnkchk-start        lambda_function.lambda_handler  2018-07-10T02:36:10.746+0000    128     e024-12d511f    arn:aws:iam::1175:role/service-role/aws-lnkchk-start    python3.6       3       $LATEST
TRACINGCONFIG   PassThrough
```
You will also need to install the python requirements for the script:

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
