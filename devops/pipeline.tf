resource "aws_s3_bucket" "pipeline_bucket" {
    bucket = "twelve-step-pipeline"
    acl = "private"
}

resource "aws_iam_role" "pipeline_role" {
    name = "twelve-step-pipeline"
    assume_role_policy = <<EOF
{
        "Version": "2012-10-17",
        "Statement": [
            {
            "Effect": "Allow",
            "Principal": {
                "Service": "codepipeline.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
            }
        ]
    }
EOF
}


resource "aws_iam_role_policy_attachment" "pipeline_role_policy_attachment" {
    role = "${aws_iam_role.pipeline_role.name}"
    policy_arn = "${aws_iam_policy.codepipeline_policy.arn}"
}


resource "aws_iam_policy" "codepipeline_policy" {
  name = "twelve-step-pipeline"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect":"Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:GetBucketVersioning",
        "s3:PutObject"
      ],
      "Resource": [
        "${aws_s3_bucket.pipeline_bucket.arn}",
        "${aws_s3_bucket.pipeline_bucket.arn}/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "codebuild:BatchGetBuilds",
        "codebuild:StartBuild"
      ],
      "Resource": "*"
    }
  ]
}
EOF
}


resource "aws_codepipeline" "twelve_step_pipeline" {
  name     = "twelve-step"
  role_arn = "${aws_iam_role.pipeline_role.arn}"

  artifact_store {
    location = "${aws_s3_bucket.pipeline_bucket.bucket}"
    type     = "S3"

  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["source_output"]

      configuration = {
        Owner  = "OLBEA20"
        Repo   = "twelve-step"
        Branch = "${var.branch_name}"
        OAuthToken = "${var.github_token}"
      }
    }
  }

  stage {
    name = "Test"

    action {
      name             = "UnitTest"
      category         = "Test"
      owner            = "AWS"
      provider         = "CodeBuild"
      input_artifacts  = ["source_output"]
      output_artifacts = ["build_output"]
      version          = "1"

      configuration = {
        ProjectName = "twelve-step-unit-test"
      }
    }
  }
}
