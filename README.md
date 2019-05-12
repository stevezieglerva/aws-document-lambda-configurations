# aws-document-lambda-configurations
Python script to gather information, including input events, for an account's AWS Lambda functions. This information is not available from a single API call. The script calls the necessary APIs and merges the results into a detailed CSV and simplified std output.

When looking to clean up and remove uncessary, redudant, and similar Lambdas, seeing all of the Lamba information, especially the input events, is very helpful.

## Prerequisites and Installation
You need to have valid credentials for connecting to AWS services. The easiest way to do this is using the AWS CLI and set up your default credentials. If you can run a basic CLI command like the following, this script should work.

```
aws lambda list-functions

FUNCTIONS       EsWTYS1B8vqM=    3678         arn:aws:lambda:us-east-1:1175:function:aws-lnkchk-start aws-lnkchk-start        lambda_function.lambda_handler  2018-07-10T02:36:10.746+0000    128     e024-12d511f    arn:aws:iam::1175:role/service-role/aws-lnkchk-start    python3.6       3       $LATEST
TRACINGCONFIG   PassThrough
```
You will also need to install the python requirements for the script:

```
pip install -r requirements.txt
```

## Execution
```
python document_lambdas.py
```

## Output

Console:
```
Getting lambda data ...
Getting lambda event sources ...
Getting S3 sources ...
Getting Cloudwatch logs ...

Function Name                       Last Run                     Last Modified                Event
-----------                         -----------                  -----------                  -----------
BingSpellcheck                      2018-10-07T12:56:12.908999   2018-03-27T17:02:50.315+0000
aws-code-index-bulk-load            2018-12-16T00:30:05.341000   2018-12-15T19:44:51.867+0000 arn:aws:sqs:us-east-1:112:code-index
aws-code-index-escape-files         2019-02-04T17:25:37.974999   2019-01-22T18:26:11.033+0000 s3:code-index-3
aws-dynamodb-to-es-bulk             2018-12-30T09:31:34.119999   2018-12-27T15:00:35.570+0000 arn:aws:dynamodb:us-east-1:112:table/elasticsearch-queue/stream/2018-12-27T13:13:11.209
```

lambda_data.csv:
A CSV file is also created with all of the detailed columns. This is useful for sorting and filtering.

## Tests
There are a few unittest tests defined to confirm the AWS API output and processing.

```
python test.py

----------------------------------------------------------------------
Ran 6 tests in 9.344s

OK
```