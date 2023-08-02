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
