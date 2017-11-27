# This script will be triggered after an S3 put event.  The expected object
# is a JSON document that contains metadata from a new twitter image.
 
# The Twitter metadata will be stored in a DynamoDB table, and the image will
# be copied to a new S3 bucket to trigger a separate Lambda function to
# run Rekognition
 
# DynamoDB Table name to store Twitter metadata
TABLE_NAME = "rekognitionTable"
# S3 Bucket name to store image, which will invoke the Rekognition script

 
import json
import boto3
import urllib
import os
import botocore
 
print('Starting function')
 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)
s3 = boto3.client('s3')
IMAGE_BUCKET_NAME = os.environ['S3RekBucket']
 
 
def lambda_handler(event, context):
 
    # Get the bucket name and key (File Name)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
 
    json_content = {}
    
   
    # Get the JSON object from S3 and parse it to a JSON string
    try:
        s3object = s3.get_object(Bucket=bucket, Key=key)
       
        # For debugging purposes
        print("s3object: " + str(s3object))
       
        # Parse the object to JSON format
        s3bodydec = s3object['Body'].read().decode()
        # Each object contains meta data from multiple tweets. These appear as separate JSON objects
        # We want to separate all the JSON objects and work with each one individually
        tweets = s3bodydec.split("}{")
        for tweet in tweets:
            record = ""
            if not tweet.startswith("{"):
                record = "{" + tweet

            else:
                record = tweet
            if not tweet.endswith("}"):
                record = record  + "}"
            print("Record = " + record)
            json_content = json.loads(record)
            
            print("Successfully received JSON object from S3: " + str(json_content))
            

            # image_url contains the fully qualified image path name, so we want to
            # parse out the filename
            image_url = json_content['image_url']
            filename = image_url.split("/")[-1]
            # We prepend the Primary Key, id_str, as part of the filename, separating it with ---
            # The id_str is used in another Lambda function to retrieve the object's record in DynamoDB
            destination = "images/" + json_content['id_str'] +'---' + filename
            # Download the image to a temp directory
            urllib.request.urlretrieve(image_url, "/tmp/"+filename )
            # Save the image from Twitter URL and write to the other S3 bucket   

             # For Debugging purposes
            print( "PUT TO S3 - Key: "+ destination + ", id_str: "+json_content['id_str'])
       
            # Put the file into the new bucket, with id_str saved as metadata
            s3.put_object(Bucket=IMAGE_BUCKET_NAME,
                Key=destination,
                Metadata={
                    'id_str':json_content['id_str']
                },
                Body=open("/tmp/"+filename, 'rb')
            )
       
            print("Successfully put image to S3")
            
            # Put the JSON conent in a new DynamoDB record
            dynamoItem={
                'id_str': json_content['id_str'],
                'loc': json_content['loc'],
                'description': json_content['description'],
                'created': json_content['created'],
                'text': json_content['text'],
                'image_url': json_content['image_url'],
                'created': json_content['user_created'],
                'user_handle': json_content['name'],
                's3_url':IMAGE_BUCKET_NAME + '/' + destination    }
            # For debugging purposes
            print("Item: " + str(dynamoItem))
       
             # Put Item to DynamoDB table
            response = table.put_item(Item=dynamoItem)
       
            print("Successfully put item to DynamoDB")
        
    
    except Exception as e:
        print("record: " + record)
        print(e)
        raise e
 
      
    return("SUCCESS")
 