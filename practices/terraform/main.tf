terraform {
    required_version = ">= 1.3.6"
}

provider aws{
  shared_config_files      = ["./conf"]
  shared_credentials_files = ["./creds"]
  profile    = "default"
}

resource "aws_instance" "web" {
  ami                    = "ami-0a6b2839d44d781b2"
  instance_type          = "t2.micro"
  vpc_security_group_ids = ["${aws_security_group.web.id}"]
  user_data              = "${file("user_data.sh")}"

  tags = {
    Name = "hello-world-web"
  }
}

resource "aws_security_group" "web" {
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
