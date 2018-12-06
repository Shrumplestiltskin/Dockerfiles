#!/home/xxx/aws/venv/bin/python3

'''
Totally hacky example of pulling TOTP from vault and issuing MFA access credentials
then making these credentials available to terraform
'''

import os
import hvac
import boto3

#set mfa_arn
mfa_arn = 'enter_arn_here'

'''
Starting interact with HVAC (hashicorp vault python3 lib)
'''
#set vault server URL + client token for interacting with vault, ACLs are tied to tokens
hvac_client = hvac.Client(url='http://xxxx:8200', token=os.environ['VAULT_TOKEN'])

#read vault location where TOTP code we want is stored
mfa_code = hvac_client.read('totp/code/my-key')['data']['code']

'''
Starting interact with boto3 aws python3 lib
'''
#What profile to use in ~/.aws/config & ~/.aws/credentials
boto_session = boto3.Session(profile_name='xxx')

#client mode is sts for MFA tokens
sts = boto_session.client('sts')

#Receive MFA Access Key / Secret Access Key / Session Token + other session vars
response = sts.get_session_token(DurationSeconds=43200, SerialNumber=mfa_arn, TokenCode=mfa_code)

access_key = response['Credentials']['AccessKeyId']
secret_access = response['Credentials']['SecretAccessKey']
session_token = response['Credentials']['SessionToken']



'''
Make the creds available to terraform
'''
#store this stuff in a generated config file that is specified in "aws provider" block in terraform 
shared_cred_file = '/home/xxx/aws/terraform/shared_cred_file_generated'

#write info to file, set this file as 'shared_credentials_file' in main.tf 
with open(shared_cred_file, 'w') as file:
    file.write('[generated_profile]\n')
    file.write('aws_access_key_id = ' + access_key + '\n')
    file.write('aws_secret_access_key = ' + secret_access + '\n')
    file.write('aws_session_token = ' + session_token + '\n')
