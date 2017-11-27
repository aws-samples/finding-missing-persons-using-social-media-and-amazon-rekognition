from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import os

print('Loading function')
this_region = os.environ['AWS_DEFAULT_REGION'];
print("region: " + this_region)

sns = boto3.client('sns')
s3 = boto3.client('s3')
ddb = boto3.resource('dynamodb')
table = ddb.Table('rekognitionTable')
# Using the table that was created from CloudFormation
rekognition = boto3.client('rekognition', this_region)

# --------------- Helper Functions to call Rekognition APIs ------------------

def detect_faces(bucket, key):
    response = rekognition.detect_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}})
    return len(response['FaceDetails'])
    
def compare_faces(bucket, sourcekey, targetkey, threshold=70):

    response = rekognition.compare_faces(
                    SourceImage={
                        'S3Object':{
                            'Bucket':bucket,
                            'Name':sourcekey
                        }
                    },
                    TargetImage={
                        'S3Object':{
                            'Bucket':bucket,
                            'Name':targetkey
                        }
                    },
                    SimilarityThreshold=threshold
                )

    message = ''
    # Retrieve the id_str (PK on DynamoDB) from the object's key
    tmp_str = targetkey.split("/")[-1]
    id_str = tmp_str.split("---")[0]
    print(id_str)

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        similarity = str(faceMatch['Similarity'])
        # Update the DynamoDB record with the additional match information
        record = table.get_item( Key={ 'id_str': id_str} )
        table.update_item(
            Key={"id_str": id_str},
            UpdateExpression="set possible_match = :m, similarity=:s",
            ExpressionAttributeValues={
                ':m':'true',
                ':s': similarity +'%'
            },
            ReturnValues="UPDATED_NEW"
        ) 

        print ("Similarity = " + similarity)
        # We also use the DynamoDB record to provide additional twitter meta data in our message back to the subscribers of our SNS Topic
        message = ('Possible match for missing person in https://'+ bucket + '.s3.amazonaws.com/' + targetkey +'\n' +
            "Image originated from " + record['Item']['user_handle'] +".\n" +
            "Posted on " + record['Item']['created'] + ".\n" +
            "Similarity of person in image to missing person : " + similarity + '%')
        # Send out (publish) a message with information about the possible match
        send_notification(message)
        
    return message

# Send(publish) message via SNS if match is detected
def send_notification(notice):
    response = sns.publish(
        # Get the SNS Topic Arn from Environment Variable set by the CloudFormation template
        TopicArn=os.environ['SNSArn'],
        Message=notice
        )

# Not used in the workshop - here for future reference
def detect_labels(bucket, key):
    response = rekognition.detect_labels(Image={"S3Object": {"Bucket": bucket, "Name": key}})

    # Sample code to write response to DynamoDB table 'MyTable' with 'PK' as Primary Key.
    # Note: role used for executing this Lambda function should have write access to the table.
    #table = boto3.resource('dynamodb').Table('MyTable')
    #labels = [{'Confidence': Decimal(str(label_prediction['Confidence'])), 'Name': label_prediction['Name']} for label_prediction in response['Labels']]
    #table.put_item(Item={'PK': key, 'Labels': labels})
    return response

# Not used in the workshop - here for future reference
def index_faces(bucket, key):
    # Note: Collection has to be created upfront. Use CreateCollection API to create a collecion.
    #rekognition.create_collection(CollectionId='BLUEPRINT_COLLECTION')
    response = rekognition.index_faces(Image={"S3Object": {"Bucket": bucket, "Name": key}}, CollectionId="BLUEPRINT_COLLECTION")
    return response


# --------------- Main handler ------------------


def lambda_handler(event, context):

    # Get the object (photograph) from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    targetFile = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    # for debugging
    print("bucket: " + bucket)
    print('targetFile: ' + targetFile)
    print("len(FaceDetails): " + str(detect_faces(bucket,targetFile)))
    
    #First we want to check if there are faces in the image from Twitter. If there are no faces, we simply delete the object from S3
    if detect_faces(bucket,targetFile)<=0:
        s3.delete_object(Bucket=bucket, Key=targetFile)
        print("No faces detected in " + targetFile + ". Deleting...")
    else:
        # Face(s) is/are present in the object
        print("Faces detected in " + targetFile)
        # We get the Missing Person photo, using the filename you provided when creating the CloudFormation stack
        sourceFile = os.environ['RefPhoto']
        print("Ref photo:" + sourceFile)
        try:
        # Calls Rekognition CompareFaces API
            response = compare_faces(bucket, sourceFile, targetFile)
            print(response)
            return response
        except Exception as e:
            print(e)
            print("Error processing object {} from bucket {}. ".format(sourceFile, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
            raise e
