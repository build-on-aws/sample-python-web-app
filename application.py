# Copyright 2015. Amazon Web Services, Inc. All Rights Reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import json

import flask
from flask import request, Response

import boto3

print("Configure the application")
# Default config vals
THEME = 'default' if os.environ.get('THEME') is None else os.environ.get('THEME')
FLASK_DEBUG = 'false' if os.environ.get('FLASK_DEBUG') is None else os.environ.get('FLASK_DEBUG')

# Create the Flask app
application = flask.Flask(__name__)

# Load config values specified above
application.config.from_object(__name__)

# Load configuration vals from a file
application.config.from_pyfile('application.config', silent=True)

# Only enable Flask debugging if an env var is set to true
application.debug = application.config['FLASK_DEBUG'] in ['true', 'True']

# Connect to DynamoDB and get refo to Table
print("Connect to DynamoDB")
ddb    = boto3.resource('dynamodb', region_name=application.config['AWS_REGION'])
client = boto3.client('dynamodb', region_name=application.config['AWS_REGION'])

@application.route('/')
def welcome():
    theme = application.config['THEME']
    return flask.render_template('index.html', theme=theme, flask_debug=application.debug)


@application.route('/signup', methods=['POST'])
def signup():
    signup_data = dict()
    for item in request.form:
        signup_data[item] = request.form[item]

    # try:
    #     store_in_dynamo(signup_data)
    # except client.exceptions.ConditionalCheckFailedException:
    #     return Response("", status=409, mimetype='application/json')

    return Response(json.dumps(signup_data), status=201, mimetype='application/json')


def store_in_dynamo(signup_data):
    table = ddb.Table(application.config['STARTUP_SIGNUP_TABLE'])
    table.put_item(
        Item=signup_data
    )
    print("PutItem succeeded:")


# def create_table():
#     ddb.create_table(
#         TableName=application.config['STARTUP_SIGNUP_TABLE'], 
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'email',
#                 'AttributeType': 'S'
#             }
#         ],
#         KeySchema=[
#             {
#                 'AttributeName': 'email',
#                 'KeyType': 'HASH'
#             }
#         ], 
#         BillingMode='PAY_PER_REQUEST'
#     )


# def init_db():
#     try:
#         print("Check DynamoDB table")
#         response = client.describe_table(TableName=application.config['STARTUP_SIGNUP_TABLE'])
#     except client.exceptions.ResourceNotFoundException as err:
#         print("DynamoDB table doesn't exist, please create as part of the guide")
#         # create_table()

if __name__ == '__main__':
    init_db()
    application.run(host='0.0.0.0')
