data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
variable "function_name" {
    type = string
}

resource "aws_api_gateway_rest_api" "api" {
    name = "throwtrash-compare"
    api_key_source = "HEADER"
    endpoint_configuration {
        types = ["REGIONAL"]
    }
    tags = {
        app = "throwtrash"
        group = "compare"
    }

    lifecycle {
      ignore_changes = [ tags ]
    }
}

resource "aws_api_gateway_stage" "api-stage-dev" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    stage_name = "dev"
    deployment_id = aws_api_gateway_deployment.api-deployment-dev.id
    variables = {
      "stageName" = "dev"
    }
    tags = {
        app = "throwtrash"
        group = "compare"
    }
    lifecycle {
      ignore_changes = [ tags ]
    }
}

resource "aws_api_gateway_stage" "api-stage-prod" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    stage_name = "prod"
    deployment_id = aws_api_gateway_deployment.api-deployment-prod.id
    variables = {
      "stageName" = "prod"
    }
    tags = {
        app = "throwtrash"
        group = "compare"
    }

    lifecycle {
      ignore_changes = [ tags ]
    }
}

resource "aws_api_gateway_resource" "api-resource" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    parent_id = aws_api_gateway_rest_api.api.root_resource_id
    path_part = "two_text_compare"
}

resource "aws_api_gateway_method" "api-method-post" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    resource_id = aws_api_gateway_resource.api-resource.id
    http_method = "POST"
    authorization = "NONE"
    api_key_required = true
}

resource "aws_api_gateway_integration" "api-integration" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    resource_id = aws_api_gateway_resource.api-resource.id
    http_method = aws_api_gateway_method.api-method-post.http_method
    integration_http_method = "POST"
    type = "AWS_PROXY"
    uri = "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/arn:aws:lambda:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:function:${var.function_name}:$${stageVariables.stageName}/invocations"
    passthrough_behavior = "WHEN_NO_MATCH"
}


resource "aws_api_gateway_deployment" "api-deployment-dev" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    depends_on = [ aws_api_gateway_integration.api-integration ]
    triggers = {
        redeployment = sha1(jsonencode([
            aws_api_gateway_integration.api-integration.id,
            aws_api_gateway_method.api-method-post.id,
            aws_api_gateway_resource.api-resource.id
        ]))
    }
}

resource "aws_api_gateway_deployment" "api-deployment-prod" {
    rest_api_id = aws_api_gateway_rest_api.api.id
    depends_on = [ aws_api_gateway_integration.api-integration ]
    triggers = {
        redeployment = sha1(jsonencode([
            aws_api_gateway_integration.api-integration.id,
            aws_api_gateway_method.api-method-post.id,
            aws_api_gateway_resource.api-resource.id
        ]))
    }
}

resource "aws_api_gateway_usage_plan" "usage-plan-dev" {
    name = "throwtrash-compare-dev-plan"
    api_stages {
        api_id = aws_api_gateway_rest_api.api.id
        stage = aws_api_gateway_stage.api-stage-dev.stage_name
    }
}

resource "aws_api_gateway_usage_plan" "usage-plan-prod" {
    name = "throwtrash-compare-prod-plan"
    api_stages {
        api_id = aws_api_gateway_rest_api.api.id
        stage = aws_api_gateway_stage.api-stage-prod.stage_name
    }
}

resource "aws_api_gateway_api_key" "api-key-dev" {
    name = "throwtrash-compare-dev-key"
}

resource "aws_api_gateway_api_key" "api-key-prod" {
    name = "throwtrash-compare-prod-key"
}

resource "aws_api_gateway_usage_plan_key" "api-plan-key-dev" {
    usage_plan_id = aws_api_gateway_usage_plan.usage-plan-dev.id
    key_type = "API_KEY"
    key_id = aws_api_gateway_api_key.api-key-dev.id
}

resource "aws_api_gateway_usage_plan_key" "api-plan-key-prod" {
    usage_plan_id = aws_api_gateway_usage_plan.usage-plan-dev.id
    key_type = "API_KEY"
    key_id = aws_api_gateway_api_key.api-key-prod.id
}

output "api_gateway_execution_arn" {
    value = aws_api_gateway_rest_api.api.execution_arn
}

output "stage_dev_name" {
    value = aws_api_gateway_stage.api-stage-dev.stage_name
}

output "stage_prod_name" {
    value = aws_api_gateway_stage.api-stage-prod.stage_name
}

output "api_resource_path" {
    value = aws_api_gateway_resource.api-resource.path
}