terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.11.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
  access_key = "AKIAV75GNDDGIWARWA44"
  secret_key = "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"
}
