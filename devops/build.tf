resource "aws_s3_bucket" "twelve_step_unit_test" {
  bucket = "twelve-step-unit-test"
  acl    = "private"
}

resource "aws_iam_role" "twelve_step_unit_test" {
  name = "twelve-step-unit-test"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "codebuild.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "codepipeline_policy_attachment" {
    role = "${aws_iam_role.twelve_step_unit_test.name}"
    policy_arn = "${aws_iam_policy.codepipeline_policy.arn}"
}

resource "aws_iam_role_policy" "twelve-step-unit-test" {
  role = "${aws_iam_role.twelve_step_unit_test.name}"

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Resource": [
        "*"
      ],
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateNetworkInterface",
        "ec2:DescribeDhcpOptions",
        "ec2:DescribeNetworkInterfaces",
        "ec2:DeleteNetworkInterface",
        "ec2:DescribeSubnets",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeVpcs"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:*"
      ],
      "Resource": [
        "${aws_s3_bucket.twelve_step_unit_test.arn}",
        "${aws_s3_bucket.twelve_step_unit_test.arn}/*"
      ]
    }
  ]
}
POLICY
}

resource "aws_codebuild_project" "twelve-step-unit-test" {
  name          = "twelve-step-unit-test"
  description   = "Unit test of twelve step"
  build_timeout = "5"
  service_role  = "${aws_iam_role.twelve_step_unit_test.arn}"

  artifacts {
    type = "CODEPIPELINE"
  }

  cache {
    type     = "S3"
    location = "${aws_s3_bucket.twelve_step_unit_test.bucket}"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:1.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"

  }
  source {
    type            = "CODEPIPELINE"
    buildspec       = "unit-test.yaml"
    report_build_status = true
  }

  tags = {
    Environment = "Test"
  }
}
