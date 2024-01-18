// 1時間に1回Lambdaを実行するためのEventBridgeを作成する

variable "tags" {
  type = "map"
  default = {
    "app" = "throwtrash"
    "group" = "compare"
  }
}

data "aws_region" "current" {}

data "aws_iam_policy_document" "eventbridge" {
  statement {
    sid       = "AllowLambdaInvoke"
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_alias.lambda-alias-prod.invoke_arn]
  }
}

resource "aws_iam_role" "eventbridge-role" {
  name = "throwtrash-compare-eventbridge-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
  tags = var.tags
}

resource "aws_iam_policy" "eventbridge-policy" {
  name        = "throwtrash-compare-eventbridge-policy"
  policy      = data.aws_iam_policy_document.eventbridge.json
  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "eventbridge-policy-attachment" {
  role       = aws_iam_role.eventbridge-role.arn
  policy_arn = aws_iam_policy.eventbridge-policy.arn
}

resource "aws_cloudwatch_event_rule" "eventbridge" {
  name                = "throwtrash-compare-eventbridge"
  schedule_expression = "rate(1 hour)"
  role_arn = aws_iam_role.eventbridge-role.arn
  tags                = var.tags
}

resource "aws_cloudwatch_event_target" "eventbridge-target" {
  rule      = aws_cloudwatch_event_rule.eventbridge.name
  target_id = "throwtrash-compare"
  arn       = aws_lambda_alias.lambda-alias-prod.invoke_arn
  input    = <<EOF
{
  "word": "ゴミ"
  "comparisons": [ "ゴミ" ]
}
EOF
}
