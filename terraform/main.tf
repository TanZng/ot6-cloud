terraform {
    required_version = "> 1.3.6"
}

provider aws{}

resource "aws_instance" "lab4-example"{
    ami = "ami-0a6b2839d44d781b2"
    instance_type = "t2.micro"
}


