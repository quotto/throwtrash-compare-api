data aws_caller_identity current {}

variable "api_gateway_execution_arn" {
    type = string
}

variable "stage_dev_name" {
    type = string
}

variable "stage_prod_name" {
    type = string
}

variable "api_resource_path" {
    type = string
}

resource aws_lambda_function "throwtrash-compare" {
    function_name = "throwtrash-compare"
    role = aws_iam_role.throwtrash-compare-lambda-role.arn
    package_type = "Image"
    image_uri = "${data.aws_caller_identity.current.account_id}.dkr.ecr.ap-northeast-1.amazonaws.com/throwtrash/compare:dev"
    timeout = 60
    architectures = ["x86_64"]
    ephemeral_storage {
        size = 512
    }
    memory_size = 512
    environment {
        variables = {
            MECABRC = "/etc/mecabrc"
        }
    }
    tags = {
        app = "throwtrash"
        group = "compare"
    }
    lifecycle {
        ignore_changes = [ tags ]
    }
}

resource aws_iam_role "throwtrash-compare-lambda-role" {
    name = "throwtrash-compare-lambda-role"
    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Effect": "Allow"
        }
    ]
}
EOF
    tags = {
        app = "throwtrash"
        group = "compare"
    }
    lifecycle {
        ignore_changes = [ tags ]
    }
}

resource "aws_iam_policy" "throwtrash-compare-lambda-policy" {
    name = "throwtrash-compare-lambda-policy"
    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "logs:CreateLogGroup",
            "Resource": "arn:aws:logs:ap-northeast-1:${data.aws_caller_identity.current.account_id}:*"
        },
        
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:logs:ap-northeast-1:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/throwtrash-compare:*"
            ]
        }
    ]
}
EOF
    tags = {
        app = "throwtrash"
        group = "compare"
    }
    lifecycle {
        ignore_changes = [ tags ]
    }
}

resource "aws_iam_role_policy_attachment" "throwtrash-compare-lambda-policy-attachment" {
    role = aws_iam_role.throwtrash-compare-lambda-role.name
    policy_arn = aws_iam_policy.throwtrash-compare-lambda-policy.arn
}

resource aws_lambda_alias "lambda-alias-dev" {
    name = "dev"
    description = "dev"
    function_name = aws_lambda_function.throwtrash-compare.function_name
    function_version = "$LATEST"
}

resource aws_lambda_alias "lambda-alias-prod" {
    name = "prod"
    description = "prod"
    function_name = aws_lambda_function.throwtrash-compare.function_name
    function_version = "$LATEST"
}


resource aws_lambda_permission "throwtrash-compare-dev" {
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.throwtrash-compare.function_name
    principal = "apigateway.amazonaws.com"
    qualifier = aws_lambda_alias.lambda-alias-dev.name
    source_arn = "${var.api_gateway_execution_arn}/${var.stage_dev_name}/POST${var.api_resource_path}"
}

resource aws_lambda_permission "throwtrash-compare-prod" {
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.throwtrash-compare.function_name
    principal = "apigateway.amazonaws.com"
    qualifier = aws_lambda_alias.lambda-alias-prod.name
    source_arn = "${var.api_gateway_execution_arn}/${var.stage_prod_name}/POST${var.api_resource_path}"
}

output "function_name" {
    value = aws_lambda_function.throwtrash-compare.function_name
}