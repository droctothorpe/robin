provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "robin-ssh-https" {
  name        = "robin-ssh-https"
  description = "allow ssh and https traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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


resource "aws_instance" "robin" {
  ami               = "ami-085925f297f89fce1"
  instance_type     = "t2.micro"
  availability_zone = "us-east-1"
  security_groups   = ["${aws_security_group.robin-ssh-https.name}"]
  tags = {
    Name = "webserver"
  }

resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.robin.id
  instance_id = aws_instance.robin.id
}

resource "aws_ebs_volume" "robin" {
  availability_zone = "us-east-1"
  size              = 1
}