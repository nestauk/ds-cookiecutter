#!/bin/bash

source "$PWD/.env.shared"

# Create bucket
aws s3api create-bucket --bucket $BUCKET --region eu-west-2 --create-bucket-configuration 'LocationConstraint=eu-west-2'

# Make private
aws s3api put-public-access-block --bucket $BUCKET --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
