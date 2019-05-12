import boto3
import json
import csv
import pysnooper
import datetime




def get_basic_lambda_data():
	boto_lamda = boto3.client("lambda")
	functions = boto_lamda.list_functions(MaxItems=50)["Functions"]
	return functions


def get_lambda_event_source_mappings():
	boto_lamda = boto3.client("lambda")
	event_sources_json = boto_lamda.list_event_source_mappings(MaxItems=50)["EventSourceMappings"]
	event_sources = {}
	for event in event_sources_json:
		function_arn = event["FunctionArn"]
		event_sources[function_arn] = event
	return event_sources


def get_s3_event_notifications():
	s3 = boto3.client("s3")
	buckets = s3.list_buckets()["Buckets"]
	s3_notifications = {}
	for bucket in buckets:
		bucket_name = bucket["Name"]
		notifications = s3.get_bucket_notification_configuration(Bucket=bucket_name)
		if "LambdaFunctionConfigurations" in notifications:
			for notification in notifications["LambdaFunctionConfigurations"]:
				lambda_arn = notification["LambdaFunctionArn"]
				notification["Bucket"] = bucket_name
				s3_notifications[lambda_arn] = notification
	return s3_notifications

@pysnooper.snoop()
def get_cloudwatch_last_events(lambda_function_names):
	logs = boto3.client("logs")
	cw_results = {}
	for function in lambda_function_names:
		log_group = "/aws/lambda/" + function
		log_stream_results = logs.describe_log_streams(logGroupName=log_group, orderBy="LastEventTime", limit=1, descending=True)
		last_event_epoch = log_stream_results["logStreams"][0]["lastEventTimestamp"]
		last_event_str = datetime.datetime.fromtimestamp(last_event_epoch/1000).strftime('%Y-%m-%d %H:%M:%S.%f')
		details = {"epoch_ms" : last_event_epoch, "date" : last_event_str}
		cw_results[function] = details
	return cw_results




def create_ordered_fieldname_list(lambda_function_json):
	first_field_names = ["FunctionName", "Description"]
	fieldnames = []
	for fieldname in first_field_names:
		fieldnames.append(fieldname)
	later_fieldnames = []
	for key in lambda_function_json:
		if key not in first_field_names:
			later_fieldnames.append(key)
	later_fieldnames.append("Event")
	later_fieldnames.append("EventDetails")
	sorted_fieldname = sorted(later_fieldnames)
	for fieldname in sorted_fieldname:
		fieldnames.append(fieldname)
	return fieldnames


def create_enhanced_lambda_list(fieldnames, functions, event_sources, s3_notifications):
	function_details = {}
	for function in functions:
		dict_to_be_written = {}
		for key, value in function.items():
			if key in fieldnames:
				dict_to_be_written[key] = value
		function_arn = function["FunctionArn"]
		event = ""
		event_details = ""
		if function_arn in event_sources:
			event_json = event_sources[function_arn]
			event = event_json["EventSourceArn"]
			event_json.pop("LastModified")
			event_details = json.dumps(event_json)
		if function_arn in s3_notifications:
			event_json = s3_notifications[function_arn]
			event = "s3:" + event_json["Bucket"]
			event_details = json.dumps(event_json)	

		dict_to_be_written["Event"]= event
		dict_to_be_written["EventDetails"]= event_details

		function_name = dict_to_be_written["FunctionName"]
		function_details[function_name] = dict_to_be_written
	return function_details



def write_csv():
	print("Getting lambda data ...")
	functions = get_basic_lambda_data()

	# Get non-S3 event sources for lambdas
	print("Getting lambda event sources ...")
	event_sources = get_lambda_event_source_mappings()

	# Get S3 event notifications for lambdas
	print("Getting S3 sources ...")
	s3_notifications = get_s3_event_notifications()

	sample_function_json = functions[0]
	fieldnames = create_ordered_fieldname_list(sample_function_json)

	function_details = create_enhanced_lambda_list(sample_function_json, functions, event_sources, s3_notifications)


	with open("lambda_data.csv", "w", newline="") as csvfile:
		sample_function_json = functions[0]
		fieldnames = create_ordered_fieldname_list(sample_function_json)	
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()

		function_details = {}
		for function in functions:
			dict_to_be_written = {}
			for key, value in function.items():
				if key in fieldnames:
					dict_to_be_written[key] = value
			function_arn = function["FunctionArn"]
			event = ""
			event_details = ""
			if function_arn in event_sources:
				event_json = event_sources[function_arn]
				event = event_json["EventSourceArn"]
				event_json.pop("LastModified")
				event_details = json.dumps(event_json)
			if function_arn in s3_notifications:
				event_json = s3_notifications[function_arn]
				event = "s3:" + event_json["Bucket"]
				event_details = json.dumps(event_json)	


			dict_to_be_written["Event"]= event
			dict_to_be_written["EventDetails"]= event_details
			writer.writerow(dict_to_be_written)

			function_name = dict_to_be_written["FunctionName"]
			function_details[function_name] = dict_to_be_written

		sorted_by_function_name = sorted(function_details)
		for function in sorted_by_function_name:
			lamda_data = function_details[function]
			print("{0:<35}\t<- {1}".format(lamda_data["FunctionName"], lamda_data["Event"]))






if __name__ == '__main__':
	write_csv()



