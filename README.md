# AWS DevOps Project - Flask API with CI/CD

[![AWS](https://img.shields.io/badge/AWS-EC2-orange)](https://aws.amazon.com/ec2/)
[![CloudFormation](https://img.shields.io/badge/IaC-CloudFormation-blue)](https://aws.amazon.com/cloudformation/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)](https://flask.palletsprojects.com/)

## 📋 Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Infrastructure Setup](#infrastructure-setup)
- [CI/CD Pipeline](#cicd-pipeline)
- [API Endpoints](#api-endpoints)
- [Monitoring & Alerts](#monitoring--alerts)
- [Screenshots](#screenshots)
- [Cleanup](#cleanup)
- [Cost Estimation](#cost-estimation)

---

## 🎯 Overview

This project demonstrates a **production-ready DevOps implementation** on AWS, featuring:
- A simple **Flask REST API** with health check and echo endpoints
- **Infrastructure as Code** using AWS CloudFormation
- **Automated CI/CD** pipeline with GitHub Actions
- **Monitoring and alerting** using CloudWatch and SNS
- **Unit testing** with pytest

**Live API Endpoint**: `http://YOUR_EC2_IP:5000`

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────────┐      ┌─────────────┐
│   GitHub    │─────▶│ GitHub Actions   │─────▶│   AWS EC2   │
│ Repository  │      │   (CI/CD)        │      │  Flask API  │
└─────────────┘      └──────────────────┘      └─────────────┘
                              │                        │
                              │                        │
                              ▼                        ▼
                     ┌──────────────┐         ┌──────────────┐
                     │ Unit Tests   │         │ CloudWatch   │
                     │   (pytest)   │         │  Logs/Alarms │
                     └──────────────┘         └──────────────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │  SNS Email   │
                                              │ Notification │
                                              └──────────────┘
```

### Components:
- **Backend**: Python Flask application
- **Infrastructure**: AWS EC2 (t3.micro), Security Groups, IAM Roles
- **IaC**: AWS CloudFormation templates
- **CI/CD**: GitHub Actions for automated testing and deployment
- **Monitoring**: CloudWatch Logs, CloudWatch Alarms, SNS notifications

---

## ✨ Features

### Part 1 - Backend API
- ✅ RESTful API with Flask
- ✅ `/health` endpoint for health checks
- ✅ `/echo` endpoint for JSON payload echo
- ✅ Unit tests with pytest
- ✅ JSON-based logging for CloudWatch

### Part 2 - AWS Infrastructure
- ✅ EC2 instance provisioned via CloudFormation
- ✅ Security Group with HTTP (5000), SSH (22) access
- ✅ IAM Role with CloudWatch permissions
- ✅ Automated deployment via GitHub Actions
- ✅ Systemd service for application management

### Part 3 - Monitoring & Logging
- ✅ CloudWatch Logs integration
- ✅ CloudWatch Agent for metrics collection
- ✅ CPU utilization alarm (threshold: 70%)
- ✅ SNS email notifications for alarms
- ✅ 7-day log retention policy

---

## 🔧 Prerequisites

### Required Tools:
- **AWS Account** with appropriate permissions
- **AWS CLI** configured with credentials
- **Git** for version control
- **Python 3.11+** for local development
- **EC2 Key Pair** for SSH access

### AWS Services Used:
- EC2, CloudFormation, CloudWatch, SNS, IAM

---

## 📁 Project Structure

```
aws-devops-project/
├── backend/
│   ├── app.py                    # Flask application
│   ├── requirements.txt          # Python dependencies
│   └── tests/
│       └── test_app.py          # Unit tests
├── infrastructure/
│   └── cloudformation/
│       └── ec2-stack.yaml       # CloudFormation template
├── .github/
│   └── workflows/
│       └── deploy.yml           # GitHub Actions workflow
├── .gitignore
└── README.md
```

---

## 💻 Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/aws-devops-project.git
cd aws-devops-project
```

### 2. Setup Virtual Environment
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

Server will start at: `http://localhost:5000`

### 5. Run Tests
```bash
pytest tests/ -v
```

### 6. Test Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Echo endpoint
curl -X POST http://localhost:5000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello DevOps!", "timestamp": "2025-10-03"}'
```

---

## 🚀 Infrastructure Setup

### Step 1: Configure AWS CLI
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Default region: us-east-1
# Default output format: json
```

### Step 2: Create EC2 Key Pair
```bash
aws ec2 create-key-pair \
  --key-name flask-api-key \
  --query 'KeyMaterial' \
  --output text > flask-api-key.pem

# Set permissions (Linux/Mac)
chmod 400 flask-api-key.pem
```

### Step 3: Deploy CloudFormation Stack
```bash
aws cloudformation create-stack \
  --stack-name flask1-api \
  --template-body file://infrastructure/cloudformation/ec2-stack.yaml \
  --parameters \
    ParameterKey=KeyName,ParameterValue=flask-api-key \
    ParameterKey=InstanceType,ParameterValue=t2.micro  \
    ParameterKey=SSHLocation,ParameterValue=YOUR_IP/32 \
    ParameterKey=EmailAddress,ParameterValue=your-email@example.com \
  --capabilities CAPABILITY_IAM \
  --region us-east-1
```

### Step 4: Monitor Stack Creation
```bash
# Check stack status
aws cloudformation describe-stacks \
  --stack-name flask1-api \
  --query 'Stacks[0].StackStatus'

# Get stack outputs
aws cloudformation describe-stacks \
  --stack-name flask1-api \
  --query 'Stacks[0].Outputs'
```

Wait for status: `CREATE_COMPLETE` (takes 3-5 minutes)

### Step 5: Confirm SNS Email Subscription
Check your email and click the confirmation link from AWS Notifications.

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

The pipeline automatically:
1. **Tests** - Runs pytest on every push/PR
2. **Deploys** - Deploys to EC2 on successful merge to `main`

### Setup GitHub Secrets

Navigate to: **Repository Settings → Secrets and variables → Actions**

Add the following secrets:

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key | `wJalr...` |
| `EC2_HOST` | EC2 public IP address | `54.123.45.67` |
| `SSH_PRIVATE_KEY` | Content of .pem file | `-----BEGIN RSA...` |

### Trigger Deployment
```bash
git add .
git commit -m "Deploy Flask API"
git push origin main
```

Watch the pipeline in: **GitHub → Actions tab**

---

## 🌐 API Endpoints

### Base URL
```
http://YOUR_EC2_IP:5000
```

### 1. Health Check
**Endpoint**: `GET /health`

**Description**: Returns the health status of the API

**Response**:
```json
{
  "status": "ok"
}
```

**Example**:
```bash
curl http://YOUR_EC2_IP:5000/health
```

### 2. Echo
**Endpoint**: `POST /echo`

**Description**: Echoes back the JSON payload sent in the request

**Request Headers**:
- `Content-Type: application/json`

**Request Body**:
```json
{
  "message": "Hello World",
  "value": 123
}
```

**Response**:
```json
{
  "message": "Hello World",
  "value": 123
}
```

**Example**:
```bash
curl -X POST http://YOUR_EC2_IP:5000/echo \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from AWS!", "timestamp": "2025-10-03"}'
```

---

## 📊 Monitoring & Alerts

### CloudWatch Logs

**Log Group**: `/aws/ec2/flask-api`

**View Logs**:
1. Go to AWS Console → CloudWatch → Log Groups
2. Select `/aws/ec2/flask-api`
3. Click on the log stream (instance ID)

**Via CLI**:
```bash
aws logs tail /aws/ec2/flask-api --follow
```

### CloudWatch Alarms

**Alarm**: `flask1-api-high-cpu`

**Configuration**:
- **Metric**: CPUUtilization
- **Threshold**: > 70%
- **Evaluation Period**: 5 minutes
- **Action**: Send SNS email notification

**View Alarm Status**:
```bash
aws cloudwatch describe-alarms --alarm-names flask1-api-high-cpu
```

### SNS Notifications

When CPU exceeds 70%, you'll receive an email notification with:
- Alarm name
- Timestamp
- Current CPU value
- Link to AWS Console

---

## 📸 Screenshots

### 1. SNS Email Notification
![SNS Notification](screenshots/sns-email.png)
*CloudWatch alarm triggered - CPU exceeded 70% threshold*

### 2. CloudWatch Alarms Dashboard
![CloudWatch Alarms](screenshots/cloudwatch-alarms.png)
*Alarm configuration showing current state: OK*

### 3. CloudWatch Overview
![CloudWatch Overview](screenshots/cloudwatch-overview.png)
*Recent alarms and EC2 service metrics*

### 4. EC2 Instance Running
![EC2 Instance](screenshots/ec2-instance.png)
*EC2 instance deployed via CloudFormation*

### 5. GitHub Actions Pipeline
![GitHub Actions](screenshots/github-actions.png)
*Successful CI/CD pipeline execution*

---

## 🧹 Cleanup

To avoid ongoing charges, delete all resources:

### Delete CloudFormation Stack
```bash
aws cloudformation delete-stack --stack-name flask1-api

# Monitor deletion
aws cloudformation wait stack-delete-complete --stack-name flask1-api
```

This will automatically delete:
- EC2 instance
- Security Group
- IAM Role & Instance Profile
- CloudWatch Log Group
- CloudWatch Alarms
- SNS Topic & Subscription

### Delete EC2 Key Pair
```bash
aws ec2 delete-key-pair --key-name flask-api-key
rm flask-api-key.pem
```

---

## 💰 Cost Estimation

### AWS Free Tier (First 12 Months)
- ✅ **EC2 t3.micro**: 750 hours/month (FREE)
- ✅ **CloudWatch**: 10 custom metrics, 10 alarms (FREE)
- ✅ **CloudWatch Logs**: 5GB ingestion, 5GB storage (FREE)
- ✅ **SNS**: 1,000 email notifications/month (FREE)

### After Free Tier
- **EC2 t3.micro**: ~$7.50/month
- **CloudWatch Logs**: ~$0.50/month (5GB storage)
- **CloudWatch Alarms**: Free (within limits)
- **Total**: ~$8/month

### Cost Optimization Tips:
- Stop EC2 instance when not in use
- Delete old CloudWatch logs
- Use AWS Budgets to set spending alerts

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|-----------|
| **Backend** | Python 3.11, Flask 3.0 |
| **Testing** | pytest, pytest-flask |
| **IaC** | AWS CloudFormation |
| **Compute** | AWS EC2 (Amazon Linux 2023) |
| **Monitoring** | AWS CloudWatch, CloudWatch Agent |
| **Notifications** | AWS SNS |
| **CI/CD** | GitHub Actions |
| **Version Control** | Git, GitHub |

---

## 📚 Documentation

- [AWS CloudFormation Docs](https://docs.aws.amazon.com/cloudformation/)
- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [AWS CloudWatch Logs](https://docs.aws.amazon.com/cloudwatch/latest/logs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

---

## 🏆 Project Highlights

✅ **Infrastructure as Code** - Fully automated infrastructure provisioning  
✅ **CI/CD Pipeline** - Automated testing and deployment  
✅ **Monitoring & Alerting** - Proactive issue detection  
✅ **Best Practices** - Security groups, IAM roles, logging  
✅ **Cost-Effective** - Runs entirely on AWS Free Tier  

---

## 👨‍💻 Author

**Your Name**  
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- AWS for comprehensive cloud services
- Flask community for the excellent web framework
- GitHub Actions for seamless CI/CD integration.

---

**Made with ❤️ for AWS DevOps Learning**

