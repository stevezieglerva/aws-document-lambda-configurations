from document_lambdas import *
import unittest
import boto3
import pysnooper

LAMBDAS_JSON =      [
		{
			"TracingConfig": {
				"Mode": "PassThrough"
			},
			"RevisionId": "e0242107-3d99-4c4e-848e-539d312d511f",
			"Role": "arn:aws:iam::112:role/service-role/lambda_example_dynamo",
			"MemorySize": 128,
			"Handler": "lambda_function.lambda_handler",
			"FunctionArn": "arn:aws:lambda:us-east-1:112:function:lambda_example_dynamo",
			"Version": "$LATEST",
			"Timeout": 3,
			"Runtime": "python3.6",
			"Description": "",
			"CodeSha256": "EsWTY66HHmY3qbqfyrnl9s4n96YXaMVtUNaeS1B8vqM=",
			"LastModified": "2018-07-10T02:36:10.746+0000",
			"FunctionName": "lambda_example_dynamo",
			"CodeSize": 3670628
		},
		{
			"TracingConfig": {
				"Mode": "PassThrough"
			},
			"RevisionId": "6dac0a5d-89cc-43d2-b558-37774906f108",
			"Role": "arn:aws:iam::112:role/LambdaStarterZieglerSet",
			"MemorySize": 128,
			"Handler": "lambda_function.lambda_handler",
			"Environment": {
				"Variables": {
					"regex_1": "[^a-zA-Z0-9\\\\n\\\\t \\\\(\\\\);\\'_\\-+\\n\\t\\{\\}\\*<>\\.@_;\\&\\/\\\\]+-;-",
					"regex_2": "\\n-;-\\\\n"
				}
			},
			"FunctionArn": "arn:aws:lambda:us-east-1:112:function:lambda_example_sqs",
			"Version": "$LATEST",
			"Timeout": 60,
			"Runtime": "python3.7",
			"Description": "",
			"CodeSha256": "R5tms8TDcJQ0W96EZqd8wbMh5iSN/0i1zya2oZ4nbL0=",
			"LastModified": "2019-01-22T18:26:11.033+0000",
			"VpcConfig": {
				"SecurityGroupIds": [],
				"VpcId": "",
				"SubnetIds": []
			},
			"FunctionName": "lambda_example_sqs",
			"CodeSize": 15841334
		},
		{
			"TracingConfig": {
				"Mode": "PassThrough"
			},
			"RevisionId": "e0242107-3d99-4c4e-848e-539d312d511f",
			"Role": "arn:aws:iam::112:role/service-role/aws-lnkchk-start",
			"MemorySize": 128,
			"Handler": "lambda_function.lambda_handler",
			"FunctionArn": "arn:aws:lambda:us-east-1:112:function:lambda_example_s3",
			"Version": "$LATEST",
			"Timeout": 3,
			"Runtime": "python3.6",
			"Description": "",
			"CodeSha256": "EsWTY66HHmY3qbqfyrnl9s4n96YXaMVtUNaeS1B8vqM=",
			"LastModified": "2018-07-10T02:36:10.746+0000",
			"FunctionName": "lambda_example_s3",
			"CodeSize": 3670628
		}
	]

EVENT_SOURCE_MAPPINGS =  {
		"arn:aws:lambda:us-east-1:112:function:lambda_example_dynamo" : {
			"LastModified": 1557338160.0,
			"State": "Enabled",
			"UUID": "557685e",
			"LastProcessingResult": "OK",
			"EventSourceArn": "arn:aws:dynamodb:us-east-1:115:table/lnkchk-queue/stream/2018-06-17T02:35:39.488",
			"StateTransitionReason": "User action",
			"BatchSize": 1,
			"FunctionArn": "arn:aws:lambda:us-east-1:112:function:lambda_example_dynamo"
		},
		"arn:aws:lambda:us-east-1:112:function:lambda_example_sqs" :
		 {
			"LastModified": 1544883946.916,
			"State": "Enabled",
			"UUID": "c17f286c",
			"EventSourceArn": "arn:aws:sqs:us-east-1:112:code-index",
			"StateTransitionReason": "USER_INITIATED",
			"BatchSize": 10,
			"FunctionArn": "arn:aws:lambda:us-east-1:112:function:lambda_example_sqs"
		}
	}

S3_NOTIFICATIONS =  {
   "arn:aws:lambda:us-east-1:112:function:lambda_example_s3": {
	  "Filter": {
		 "Key": {
			"FilterRules": [
			   {
				  "Value": "es-bulk-files-input/4",
				  "Name": "Prefix"
			   }
			]
		 }
	  },
	  "Id": "bad40b24-c2f5-44dd-ac2e-b378e384fb85",
	  "Events": [
		 "s3:ObjectCreated:*"
	  ],
	  "LambdaFunctionArn": "arn:aws:lambda:us-east-1:112:function:lambda_example_s3",
	  "Bucket": "code-index"
   }
}



class Tests(unittest.TestCase):
	def test_get_basic_lambda_data__valid_aws_account_info__expected_json_returned_from_AWS(self):
		# Arrange

		# Act
		results = get_basic_lambda_data()

		# Assert
		self.assertTrue(len(results) > 0)
		self.assertTrue("FunctionName" in results[0])


	def test_get_lambda_event_source_mappings__valid_aws_account_info__expected_json_returned_from_AWS(self):
		# Arrange

		# Act
		results = get_lambda_event_source_mappings()

		# Assert
		self.assertTrue(len(results) > 0)
		first_key = next(iter(results))
		first_item = results[first_key]
		self.assertTrue("EventSourceArn" in first_item)


	def test_get_s3_event_notifications__valid_aws_account_info__expected_json_returned_from_AWS(self):
		# Arrange

		# Act
		results = get_s3_event_notifications()

		# Assert
		self.assertTrue(len(results) > 0)
		first_key = next(iter(results))
		first_item = results[first_key]
		self.assertTrue("LambdaFunctionArn" in first_item)

	def test_get_cloudwatch_last_events__valid_aws_account_info__expected_json_returned_from_AWS(self):
		# Arrange

		# Act
		results = get_cloudwatch_last_events(["aws-code-index-format-files", "aws-s3-to-es"])

		# Assert
		self.assertGreater(results["aws-code-index-format-files"], 0)
		self.assertGreater(results["aws-s3-to-es"], 0)



	def test_create_ordered_fieldname_list__valid_json_input__expected_fields_in_right_order(self):
		# Arrange
		sample_json_fields = {
							"key1" : "value1",
							"key2" : "value2"
							}

		# Act
		results = create_ordered_fieldname_list(sample_json_fields)

		# Assert
		self.assertEqual(results[0], "FunctionName")
		self.assertEqual(results[1], "Description")
		self.assertTrue("Event" in results)


	def test_create_enhanced_lambda_list__valid_inputs__merged_dictionary_returned(self):
		# Arrange
		lambda_basics = LAMBDAS_JSON
		event_sources = EVENT_SOURCE_MAPPINGS
		s3_notifications = S3_NOTIFICATIONS
		sample_function_json = lambda_basics[0]
		fieldnames = create_ordered_fieldname_list(sample_function_json)

		# Act
		results = create_enhanced_lambda_list(fieldnames, lambda_basics, event_sources, s3_notifications)

		# Assert
		self.assertTrue(len(results) > 0)
		self.assertEqual(results["lambda_example_dynamo"]["Event"], "arn:aws:dynamodb:us-east-1:115:table/lnkchk-queue/stream/2018-06-17T02:35:39.488")
		self.assertEqual(results["lambda_example_s3"]["Event"], "s3:code-index")

if __name__ == '__main__':
	unittest.main()	
