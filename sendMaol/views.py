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

class handle_delivery_notification(APIView):
    def get(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        try:
            with open("sendMaol/readme.md", 'a') as readme_file:
                readme_file.write(f"get method is not valid\n")
 
            return Response({"status":400, "message":"method not valid"},status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        try:
            if request.method == 'POST':
                notification_data = json.loads(request.body)
                print(notification_data)
                
                # Extract delivery information from the notification
                mail_message_id = notification_data['mail']['messageId']
                delivery_timestamp = notification_data['delivery']['timestamp']
                delivery_recipients = notification_data['delivery']['recipients']
                
                # You can perform actions based on the delivery notification here
                # For example, log the delivery status or update your database
                with open("sendMaol/readme.md", 'a') as readme_file:
                    readme_file.write(f"mail_message_id : {mail_message_id} , delivery_timestamp : {delivery_timestamp} , delivery_recipients: {delivery_recipients} \n")
                
                print(f"Delivery Notification for Message ID: {mail_message_id}")
                print(f"Delivery Timestamp: {delivery_timestamp}")
                print(f"Delivery Recipients: {delivery_recipients}")

                return Response({"status":200, "message":"success"},status=status.HTTP_200_OK)
            else:
                return Response({"status":400, "message":"method not valid"},status=status.HTTP_400_BAD_REQUEST)


        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)



class aws_ses(APIView):
    def get(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        import boto3
        try:
            
            def send_email_with_template(template_name, recipient_email, sender_email, template_data):
                session = boto3.Session(
                aws_access_key_id='AKIAXBPY5MDZIBHNXH6L',
                aws_secret_access_key='knoTzCMoDL8c9xzTGmqiauwpVxTtWerWOuZC4vCn',
                region_name='ap-south-1'  # Change to your desired region
                 )
                ses = session.client('ses', region_name='ap-south-1')  # Change the region as needed

                # Send email with template
                print("sending email")
                print(template_name,"template_name")
                print(recipient_email,"recipient_email")
                print(sender_email,"sender_email")
                print(template_data,"template_data")
                subject = 'Test Email'
                body = 'This is the body of the email.'
                response = ses.send_email(
                    Source=sender_email,
                    Destination={'ToAddresses': [recipient_email]},
                    Message={
                        'Subject': {'Data': subject},
                        'Body': {'Text': {'Data': body}}
                    }
                )
                print(response)
                print("Email sent:", response['MessageId'])


                # # Get the email delivery status
                message_id = response['MessageId']
                # delivery_status = get_email_delivery_status(ses, "01090189d6beb5f0-59d1c873-2b11-4e5d-bd41-f353540b402e-000000")
                # return delivery_status

            def get_email_delivery_status(ses, message_id):
                print("delivery status")
                response = ses.get_send_email_status(
                    MessageId=message_id
                )
                return response['SendEmailStatus']

            template_name = 'test'
            recipient_email = 'hoqueaktarul07@gmail.com'
            sender_email = 'support@mypustak.com'
            template_data = '{"name": "John Doe"}'

            delivery_status = send_email_with_template(template_name, recipient_email, sender_email, template_data)
            print("Email delivery status:", delivery_status)
            # def check_aws_credentials():
            #     session = boto3.Session(
            #     aws_access_key_id='AKIAXBPY5MDZIBHNXH6L',
            #     aws_secret_access_key='knoTzCMoDL8c9xzTGmqiauwpVxTtWerWOuZC4vCn',
            #     region_name='ap-south-1'  # Change to your desired region
            #      )
            #     try:
            #         ses = session.client('ses', region_name='ap-south-1')  # Change the region as needed
            #         response = ses.list_identities()
            #         print(response,"res--------------------")
            #         return True
            #     except Exception as e:
            #         print("Error:", e)
            #         return False

            # if check_aws_credentials():
            #     print("AWS credentials found and valid.")
            # else:
            #     print("AWS credentials not found or invalid.")
                
            return Response({"status":200, "message":"Email send succesfully"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)


class track_image(APIView):
    def get(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        try:
            import boto3
            image_data=""
            # with open('C:\Users\satta\OneDrive\Desktop\office\mypustak\newEmailServer\email_server\imge\dumy+book.png') as image_file:
            #     image_data = image_file.read()

            # Set up your AWS credentials and region
            aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
            aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
            region_name = 'ap-south-1'  # Replace with your desired AWS region

            # Create an S3 client
            s3_client = boto3.client('s3', region_name=region_name,
                                    aws_access_key_id="AKIAJ3U7NNEUATYWGCWQ",
                                    aws_secret_access_key="wdh+F7u1Jz5r908G5JcYsO2uYHlIcJQ2DkmsuI7t")

            # Upload the tracking pixel (1x1 transparent image) to your S3 bucket
            bucket_name = 'https://mypustak-6.s3.amazonaws.com'
            object_key = 'dumy+book.png'
            print(image_data,"image_data++++++++++++++++++++++++")
            # image_data/ = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x8d\x8f&\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x04\x00\x01\xe3?\xa1\xbc\x00\x00\x00\x00IEND\xaeB`\x82'
            s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=image_data)

            # Print the URL of the hosted tracking pixel
            tracking_pixel_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{object_key}"
            print("Tracking pixel URL:", tracking_pixel_url)

            
            return Response({"status":200, "message":"Email send succesfully"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)


class aws_sns(APIView):
    def get(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        try:
            print("enter")
            # Set up your AWS credentials and region
            aws_access_key_id = 'AKIAXBPY5MDZIBHNXH6L'
            aws_secret_access_key = 'knoTzCMoDL8c9xzTGmqiauwpVxTtWerWOuZC4vCn'
            region_name = 'ap-south-1'  # Replace with your desired AWS region

            # Create an SNS client
            sns_client = boto3.client('sns', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

            # Subscribe to the SNS topic for bounce and complaint notifications
            topic_arn = 'arn:aws:sns:ap-south-1:484242710770:email_campaign'
            subscription = sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',  # You can choose other protocols if needed
                Endpoint='hoqueaktarul07@gmail.com'  # Your email or endpoint to receive notifications
            )

            print("Subscription ARN:", subscription)

            # Handle notifications
            print(sns_client)
            # while True:
                # response = sns_client.receive_message(TopicArn=topic_arn)
                # for message in response.get('Messages', []):
                #     notification = json.loads(message['Body'])
                #     # Process the notification, which contains bounce or complaint information
                #     print("Received notification:", notification)

                #     # Delete the processed message
                #     sns_client.delete_message(
                #         QueueUrl=topic_arn,
                #         ReceiptHandle=message['ReceiptHandle']
                    # )
            

        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)


