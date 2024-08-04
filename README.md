# Alembic Migrations with AWS Lambda

This repository provides a setup for running Alembic database migrations via AWS Lambda. The script is designed to handle various Alembic commands through AWS Lambda's test command panel.

## Prerequisites

1. **Python 3.x**
2. **AWS Account**
3. **Alembic installed**

## Files

- `lambda_handler.py`: The main Lambda handler script.
- `alembic.ini`: Alembic configuration file.
- `env.py`: Environment configuration script for Alembic.

## Setup Instructions

### Step 1: Install Dependencies

Make sure you have the necessary dependencies installed. You can create a virtual environment and install Alembic.

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install alembic
```

### Step 2: Configure Alembic
Edit the alembic.ini file to configure your database connection.

```bash
# alembic.ini
[alembic]
script_location = alembic
sqlalchemy.url = <your-database-url>
```
### Step 3: Create the Deployment Package
Package your project, including all dependencies.

```bash
zip -r9 deployment-package.zip lambda_handler.py alembic.ini env.py
zip -r9 deployment-package.zip venv/lib/python3.x/site-packages/  # Adjust the path according to your virtual environment
```

### Step 4: Create the Lambda Function
- Go to the AWS Management Console.
- Navigate to the Lambda service.
- Create a new Lambda function.
- Upload the deployment package created in Step 3.
- Set the handler to lambda_handler.lambda_handler.

### Step 5: Configure IAM Permissions
Ensure your Lambda function has the necessary IAM role with permissions to access your database.

### Step 6: Test the Lambda Function

You can test your Lambda function using the AWS Lambda test command panel. Here are some example events you can use:

### Upgrade to the Latest Revision
```bash
{
    "command": "upgrade",
    "revision": "head"
}
```

### Downgrade to the Previous Revision
```bash
{
    "command": "downgrade",
    "revision": "-1"
}
```

### Create a New Revision
```bash
{
    "command": "revision",
    "message": "Add new table"
}
```
### Show Migration History
```bash
{
    "command": "history"
}
```

### Show Verbose Migration History

```bash
{
    "command": "vhistory"
}
```

### Steps
Add the above commands to the test panel of the lambda function for executing the commands
