#!/bin/bash

# # Configuration variables
# USERNAME="USERNAME - USER EMAIL"
# PASSWORD="USER PASSWORD"
# CLIENT_ID="<CLIENT_id FOR API GATEWAY AUTH>"
# CLIENT_SECRET="<CLIENT SECRET>"

# # 1. Compute the SECRET_HASH using system python3 (bypassing pyenv)
# SECRET_HASH=$(/usr/bin/python3 -c "
# import hmac, hashlib, base64
# user, cid, secret = '$USERNAME', '$CLIENT_ID', '$CLIENT_SECRET'
# message = (user + cid).encode('utf-8')
# key = secret.encode('utf-8')
# digest = hmac.new(key, message, digestmod=hashlib.sha256).digest()
# print(base64.b64encode(digest).decode())
# ")

# # 2. Get your JWT token from Cognito
# TOKEN=$(aws cognito-idp initiate-auth \
#     --client-id "$CLIENT_ID" \
#     --auth-flow USER_PASSWORD_AUTH \
#     --auth-parameters USERNAME="$USERNAME",PASSWORD="$PASSWORD",SECRET_HASH="$SECRET_HASH" \
#     --query 'AuthenticationResult.IdToken' \
#     --output text)

# # 3. Call your secure API Gateway endpoint
# curl -X POST https://49rpde24e7.execute-api.us-east-1.amazonaws.com/train \
#      -H "Content-Type: application/json" \
#      -H "Authorization: Bearer $TOKEN" \
#      -d '{
#        "s3_input_path": "s3://customer-data-pushkar-khairnar-108372347/griffin_model/",
#        "s3_output_path": "s3://customer-data-pushkar-khairnar-108372347/output/"
#      }'


# Configuration variables
USERNAME="USERNAME - USER EMAIL"
PASSWORD="USER PASSWORD"
CLIENT_ID="<CLIENT_id FOR API GATEWAY AUTH>"

# 1. Get your JWT token directly from Cognito (No secret or hash required!)
TOKEN=$(aws cognito-idp initiate-auth \
    --client-id "$CLIENT_ID" \
    --auth-flow USER_PASSWORD_AUTH \
    --auth-parameters USERNAME="$USERNAME",PASSWORD="$PASSWORD" \
    --query 'AuthenticationResult.IdToken' \
    --output text)

# 2. Call your secure API Gateway endpoint
curl -X POST https://49rpde24e7.execute-api.us-east-1.amazonaws.com/train \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{
       "s3_input_path": "s3://customer-data-pushkar-khairnar-108372347/griffin_model/",
       "s3_output_path": "s3://customer-data-pushkar-khairnar-108372347/output/"
     }'