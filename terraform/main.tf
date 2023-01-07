terraform {
    required_version = ">= 1.3.6"
}

# Configure AWS provider
provider "aws" {
  shared_config_files      = ["./conf"]
  shared_credentials_files = ["./creds"]
  profile    = "default"
}

# Create an EC2 instance
resource "aws_instance" "project_ec2" {
  ami           = "ami-0b93ce03dcbcb10f6"
  instance_type = "t2.micro"
  iam_instance_profile = aws_iam_instance_profile.scrapy_profile.name
  vpc_security_group_ids = ["${aws_security_group.project_sg.id}"]
  key_name = "terraform_ec2_key"

  # Run a script to install dependencies and download the main script
  user_data = <<EOF
#!/bin/bash

apt-get update
apt-get install -y python3-pip git curl

# Create directory
mkdir -p /opt/repo
mkdir -p /var/log/cron

# Clone scraper and install requirements.txt
git clone https://github.com/TanZng/ot6-cloud.git /opt/repo
cd /opt/repo/project
pip3 install -r requirements.txt

# Create a cron job to run the scraper at 12am and 12pm
sudo service cron start

echo "0 */12 * * * (/bin/bash /opt/repo/crawl.sh 2>&1) > /var/log/cron/spider_log.log" | crontab

EOF

  tags = {
    Name = "project-ec2"
  }
}

# Create ssh key to get into the ec2 instance
resource "aws_key_pair" "terraform_ec2_key" {
	key_name = "terraform_ec2_key"
	public_key = "${file("terraform_ec2_key.pub")}"
}

# Create a security group
resource "aws_security_group" "project_sg" {
  name = "project-sg"
  description = "Allow HTTP and SSH traffic via Terraform"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an s3 bucket
resource "aws_s3_bucket" "project_s3" {
  bucket_prefix = "project-s3"
}

# Create DynamoDB table 
resource "aws_dynamodb_table" "project-dynamodb" {
  name           = "project-dynamodb"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "ProductId"

  attribute {
    name = "ProductId"
    type = "S"
  }
}

# Create an instance profile
resource "aws_iam_instance_profile" "scrapy_profile" {
  name = "scrapy_profile"
  role = aws_iam_role.ec2_role.name
}

# Create a role that can be assumed by an EC2 instance
resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

# Attach policies to the role
resource "aws_iam_role_policy_attachment" "role-policy-attachment" {
  for_each = toset([
    "arn:aws:iam::aws:policy/AmazonEC2FullAccess", 
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  ])

  role       = aws_iam_role.ec2_role.name
  policy_arn = each.value
}
