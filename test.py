from document_lambdas import *
import unittest
import boto3


class Tests(unittest.TestCase):
	def test_get_basic_lambda_data__valid_aws_account_info__expected_json(self):
		# Arrange

		# Act
		results = get_basic_lambda_data()

		# Assert
		self.assertTrue(len(results) > 0)
		self.assertTrue("FunctionName" in results[0])


	def test_get_lambda_event_source_mappings__valid_aws_account_info__expected_json(self):
		# Arrange

		# Act
		results = get_lambda_event_source_mappings()

		# Assert
		self.assertTrue(len(results) > 0)
		first_key = next(iter(results))
		first_item = results[first_key]
		self.assertTrue("EventSourceArn" in first_item)


	def test_get_s3_event_notifications__valid_aws_account_info__expected_json(self):
		# Arrange

		# Act
		results = get_s3_event_notifications()

		# Assert
		self.assertTrue(len(results) > 0)
		first_key = next(iter(results))
		first_item = results[first_key]
		self.assertTrue("LambdaFunctionArn" in first_item)


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
		lambda_basics = get_basic_lambda_data()
		event_sources = get_lambda_event_source_mappings()
		s3_notifications = get_s3_event_notifications()

		# Act
		results = create_enhanced_lambda_list(lambda_basics, event_sources, s3_notifications)

		# Assert
		self.assertTrue(len(results) > 0)

if __name__ == '__main__':
	unittest.main()	
