terraform {
    required_version = "> 1.3.6"
}
provider aws{
    shared_credentials_files = ["iduhfqiufh"]
    region = "fwhiquh"
}

resource "aws_instance" "lab3-example"{
    ami = "ami-iwhfiqwuf"
    instance_type = "t2.micro"
}