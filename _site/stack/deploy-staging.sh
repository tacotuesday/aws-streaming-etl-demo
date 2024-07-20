#!/usr/bin/env bash
# chmod +x ./deploy_live.sh
# Run ./deploy_live.sh
PROFILE=grafton
STACK_NAME=YourStackNameLive
LAMBDA_BUCKET=tacotuesday-s3-bucket
 
date
TIME=`date +"%Y%m%d%H%M%S"`
 
base=${PWD##*/}
zp=$base".zip"
echo $zp
 
rm -f $zp

pip install --target ./package -r requirements.txt

cd package
zip -r ../${base}.zip .

cd $OLDPWD

zip -r $zp ./events_connector -x __pycache__
 
aws --profile $PROFILE s3 cp ./${base}.zip s3://${LAMBDA_BUCKET}/events_connector/${base}${TIME}.zip

aws --profile $PROFILE \
cloudformation deploy \
--template-file stack_cicd_service_and_role.yaml \
--stack-name $STACK_NAME \
--capabilities CAPABILITY_IAM \
--parameter-overrides \
"StackPackageS3Key"="events_connector/${base}${TIME}.zip" \
"Environment"="staging" \
"Testing"="false" \