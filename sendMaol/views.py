from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
import boto3
import json
from botocore.exceptions import BotoCoreError, ClientError
from http.server import HTTPServer, BaseHTTPRequestHandler
# Create a new SES client
ses_client = boto3.client('ses', region_name='ap-south-1',
                         aws_access_key_id="AKIAXBPY5MDZIBHNXH6L",
                         aws_secret_access_key='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')

class sendSesMail(APIView):
    def get(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        try:
            subject = 'Hello from Django and AWS SES'
            message = 'This is the content of the email.'
            from_email = 'support@mypustak.com'
            recipient_list = ['hoqueaktarul07@gmail.com']

            ses_client = boto3.client('ses',
                             aws_access_key_id='AKIAXBPY5MDZIBHNXH6L',
                             aws_secret_access_key='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',
                             region_name='ap-south-1')
            response = ses_client.send_email(
                Source=from_email,
                Destination={
                    'ToAddresses': recipient_list,
                },
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': message}},
                }
            )
            print("Email sent successfully. Response:", response)



            return Response({"status":200, "message":"Email send succesfully"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)

class sendBulkMail(APIView):
    def get(self, request):
        try:
            print("api hit")
            recipients = ['hoqueaktarul07@gmail.com', 'vvozet@gmail.com',"test@gmail.com"]

            # Common email parameters
            email_subject = 'Your Subject'
            email_body = 'Hello, this is the email body.'

            # Send emails
            response = ses_client.send_bulk_templated_email(
                Source='support@mypustak.com',  # Sender's email address
                Template='TEST_TEMPLATE',  # Replace with your template name
                DefaultTemplateData='{}',
                ConfigurationSetName="test",
                Destinations=[
                    {'Destination': {'ToAddresses': [recipient]},
                    'ReplacementTemplateData': "{}"
                    }  # JSON data for template variables
                    for recipient in recipients
                ]
            )

            # Print Message IDs for each sent email
            resDatas=[]
            for result in response['Status']:
                obj={"sendStatus":result['Status'],'MessageId':result['MessageId']}
                resDatas.append(obj)

            for index, value in enumerate(recipients):
                resDatas[index]["email"]=value
            

            return Response({"status":200, "response":resDatas},status=status.HTTP_200_OK)

        except (BotoCoreError, ClientError) as e:
            print(f"Error: {e}")
            return Response({"status":400, "message":f"Error: {e}"},status=status.HTTP_400_BAD_REQUEST)

class updateStatus(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.headers['x-amz-sns-message-type'] == 'SubscriptionConfirmation':
            # Handle subscription confirmation
            subscription_info = json.loads(post_data)
            subscribe_url = subscription_info['SubscribeURL']
            
            # Send a GET request to the SubscribeURL to confirm subscription
            # Example: requests.get(subscribe_url)
            # Don't forget to handle the response appropriately

            # Respond to SNS with HTTP 200 OK
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('Subscription confirmed.'.encode())

    # host = 'http://127.0.0.1:8000'  # Host or IP address to listen on
    # port = 8000  # Port number to listen on

    # server_address = (host, port)
    # httpd = HTTPServer(server_address, MyHandler)
    # httpd.serve_forever()
class SNSEndpoint(APIView):
    def post(self, request):
        try:
            # Initialize SNS client
            sns_client = boto3.client(
                'sns',
                aws_access_key_id='AKIAXBPY5MDZIBHNXH6L',  # Replace with your AWS access key
                aws_secret_access_key='knoTzCMoDL8c9xzTGmqiauwpVxTtWerWOuZC4vCn',  # Replace with your AWS secret key
                region_name='ap-south-1'  # Replace with your AWS region
            )

            # Create an SNS topic
            topic_response = sns_client.create_topic(Name='MyTopic')
            topic_arn = topic_response['TopicArn']

            # Subscribe to the topic using HTTP protocol
            endpoint = 'http://localhost:8000/sendMail/updateStatus'  # Replace with your HTTP endpoint URL
            subscription_response = sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='http',
                Endpoint=endpoint
            )

            # Publish a message to the topic
            message = 'Hello from SNS!'
            publish_response = sns_client.publish(
                TopicArn=topic_arn,
                Message=message
            )

            return Response(
                {
                    "status": 200,
                    "topic_response": topic_response,
                    "subscription_response": subscription_response,
                    "publish_response": publish_response
                },
                status=status.HTTP_200_OK
            )

        except (BotoCoreError, ClientError) as e:
            print(f"Error: {e}")
            return Response({"status": 400, "message": f"Error: {e}"}, status=status.HTTP_400_BAD_REQUEST)

