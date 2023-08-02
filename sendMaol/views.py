from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status

class sendMail(APIView):
    def get(self, request):
        from django.core.mail import send_mail
        from django.conf import settings
        from django.template.loader import render_to_string,get_template
        import time
        try:
            message = 'TEST EMAIL'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ["hoqueaktarul07@gmail.com"]
            # msg_html = render_to_string('test.html',{}) #### passing data1 and data2 to the html file common_email.html
            msg_html = get_template('test.html').render({}) #### passing data1 and data2 to the html file common_email.html
            
            send_mail('mail for test',message,email_from,recipient_list,html_message=msg_html,fail_silently=False,) ### command to send thhe email
            return Response({"status":200, "message":"Email send succesfully"},status=status.HTTP_200_OK)

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
                aws_access_key_id='AKIAJ3U7NNEUATYWGCWQ',
                aws_secret_access_key='wdh+F7u1Jz5r908G5JcYsO2uYHlIcJQ2DkmsuI7t',
                region_name='ap-south-1'  # Change to your desired region
                 )
                ses = session.client('ses', region_name='ap-south-1')  # Change the region as needed

                # Send email with template
                print("sending email")
                print(template_name,"template_name")
                print(recipient_email,"recipient_email")
                print(sender_email,"sender_email")
                print(template_data,"template_data")
                response = ses.send_templated_email(
                    Source=sender_email,
                    Destination={
                        'ToAddresses': [recipient_email],
                    },
                    Template=template_name,
                    TemplateData=template_data
                )

                # Get the email delivery status
                message_id = response['MessageId']
                delivery_status = get_email_delivery_status(ses, message_id)
                return delivery_status

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
            #     aws_access_key_id='AKIAJ3U7NNEUATYWGCWQ',
            #     aws_secret_access_key='wdh+F7u1Jz5r908G5JcYsO2uYHlIcJQ2DkmsuI7t',
            #     region_name='ap-south-1'  # Change to your desired region
            #      )
            #     try:
            #         ses = session.client('ses', region_name='ap-south-1')  # Change the region as needed
            #         response = ses.list_identities()
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

            # Set up your AWS credentials and region
            aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
            aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
            region_name = 'us-west-2'  # Replace with your desired AWS region

            # Create an S3 client
            s3_client = boto3.client('s3', region_name=region_name,
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)

            # Upload the tracking pixel (1x1 transparent image) to your S3 bucket
            bucket_name = 'your-s3-bucket-name'
            object_key = 'tracking_pixel.png'
            image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90\x8d\x8f&\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00\x04\x00\x01\xe3?\xa1\xbc\x00\x00\x00\x00IEND\xaeB`\x82'
            s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=image_data)

            # Print the URL of the hosted tracking pixel
            tracking_pixel_url = f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{object_key}"
            print("Tracking pixel URL:", tracking_pixel_url)

            
            return Response({"status":200, "message":"Email send succesfully"},status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"status":400, "message":"Email send unsuccesfully"},status=status.HTTP_400_BAD_REQUEST)

