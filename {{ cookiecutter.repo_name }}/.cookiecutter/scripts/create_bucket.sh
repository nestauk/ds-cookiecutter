#!/bin/bash
set -u

function create_bucket() {
    echo "Attempting creation of bucket $1 ..."

    aws s3api create-bucket\
    --bucket "$1"\
    --region eu-west-2\
    --create-bucket-configuration\
    'LocationConstraint=eu-west-2';
}

function make_bucket_private() {
    echo "Configuring $1 to block all public access...";

    aws s3api put-public-access-block\
    --bucket "$1"\
    --public-access-block-configuration\
    "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true";
}
