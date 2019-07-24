terraform {
  backend "s3" {
    bucket = "twelve-step-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
