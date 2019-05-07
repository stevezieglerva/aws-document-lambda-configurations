import boto3
import json
import csv
import pysnooper



test = {
    "LambdaFunctionConfigurations": [
        {
            "Id": "a452521e-0cfc-46a7-8e46-aef266f37406",
            "Events": [
                "s3:ObjectCreated:*"
            ],
            "Filter": {
                "Key": {
                    "FilterRules": [
                        {
                            "Name": "Prefix",
                            "Value": "prep-output"
                        }
                    ]
                }
            },
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:112280397275:function:aws-code-index-format-files"
        },
        {
            "Id": "555f4c3e-ba7b-4e6f-9884-71e1c797ff8f",
            "Events": [
                "s3:ObjectCreated:*"
            ],
            "Filter": {
                "Key": {
                    "FilterRules": [
                        {
                            "Name": "Prefix",
                            "Value": "es-bulk-files-input/2"
                        }
                    ]
                }
            },
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:112280397275:function:aws-read-s3-es-events-in-chunks-s2"
        }]
}


def write_csv():

	boto_lamda = boto3.client("lambda")
	functions = boto_lamda.list_functions(MaxItems=50)["Functions"]

	# Get non-S3 event sources for lambdas
	event_sources_json = boto_lamda.list_event_source_mappings(MaxItems=50)["EventSourceMappings"]
	event_sources = {}
	for event in event_sources_json:
		function_arn = event["FunctionArn"]
		event_sources[function_arn] = event

	# Get S3 event notifications for lambdas
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

	with open("lambda_data.csv", "w", newline="") as csvfile:
		first_field_names = ["FunctionName", "Description"]
		fieldnames = []
		for fieldname in first_field_names:
			fieldnames.append(fieldname)
		later_fieldnames = []
		for key in functions[0]:
			if key not in first_field_names:
				later_fieldnames.append(key)
		later_fieldnames.append("Event")
		later_fieldnames.append("EventDetails")
		sorted_fieldname = sorted(later_fieldnames)
		for fieldname in sorted_fieldname:
			fieldnames.append(fieldname)
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

		writer.writeheader()
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

			print("{0:<35}\t<- {1}".format(dict_to_be_written["FunctionName"], dict_to_be_written["Event"]))



write_csv()






