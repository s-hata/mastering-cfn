#!/bin/sh

set -e

aws s3 sync . s3://ignite-cfn-template-store3/examples/mastering-cfn/continuous-deploy-01


