#!/bin/sh

set -e

STACK_NAME="mastering-cfn-continuous-deploy-01"

aws s3 sync . s3://ignite-cfn-template-store3/examples/mastering-cfn/continuous-deploy-01

aws cloudformation create-stack \
  --stack-name $STACK_NAME \
  --template-url https://s3.amazonaws.com/ignite-cfn-template-store3/examples/mastering-cfn/continuous-deploy-01/pipeline/src/cft/root.yml \
  --on-failure DO_NOTHING \
  --capabilities CAPABILITY_NAMED_IAM
aws cloudformation wait \
  stack-create-complete \
  --stack-name $STACK_NAME
