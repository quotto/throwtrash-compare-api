terraform {
    backend "s3" {
      bucket = "throwtrash-tfstate-ap-northeast-1"
      key    = "compare.tfstate"
      region = "ap-northeast-1"
    }
}

provider "aws" {
  region = "ap-northeast-1"
}

module "api" {
  source = "./api"
  function_name = module.lambda.function_name
}
module "lambda" {
  source = "./lambda"
  api_gateway_execution_arn = module.api.api_gateway_execution_arn
  stage_dev_name = module.api.stage_dev_name
  stage_prod_name = module.api.stage_prod_name
  api_resource_path = module.api.api_resource_path
}