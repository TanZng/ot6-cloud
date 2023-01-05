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
  vpc_security_group_ids = ["${aws_security_group.project_sg.id}"]
  key_name = "terraform_ec2_key"

  # Run a script to install dependencies and download the main script
  user_data = <<EOF
#!/bin/bash

apt-get update
apt-get install -y python3-pip git curl

# Replace this with our script and requirements.txt
git clone https://github.com/TanZng/ot6-cloud.git
pip3 install -r requirements.txt

# Copy main script
mkdir -p /opt/app
cp final_project_scraper.py /opt/app/

# Create a cron job to run the main.py script every minute
# TODO: change how often run the script
sudo service cron start

echo "* * * * * /usr/bin/python3 /opt/app/final_project_scraper.py >> /scrapy.log" | crontab

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

resource "random_uuid" "uuid" {}

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