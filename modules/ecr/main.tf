# ECR Repository
resource "aws_ecr_repository" "flask_app" {
  name = "flask-app"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "flask-app"
  }
}

resource "aws_ecr_repository" "react_app" {
  name = "react-app"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "react-app"
  }
}