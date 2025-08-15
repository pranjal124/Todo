import boto3
import json

def get_secret(secret_name):
    region = "ap-south-1"  # replace with your region
    client = boto3.client("secretsmanager", region_name=region)

    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_dict = json.loads(response['SecretString'])
        return secret_dict
    except Exception as e:
        print("❌ Error retrieving secret:", e)
        return {}

# Usage
secret = get_secret("/myapp/db-credentials")
print(secret)

# Example:
DB_HOST = secret["host"]
DB_USER = secret["username"]
DB_PASSWORD = secret["password"]
DB_NAME = secret["dbname"]

# DB_HOST = "task-app-db.c3eoey2kcevb.us-west-2.rds.amazonaws.com"
# DB_NAME = "tasks"
