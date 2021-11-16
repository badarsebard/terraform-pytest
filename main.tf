terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>3.64"
    }
  }
}

resource "aws_s3_bucket" "my_test_bucket" {
  bucket = "my-test-bucket"
}

provider "aws" {
  access_key = "my-access-key"
  secret_key = "my-secret-key"
}
