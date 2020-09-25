# twitter stream cfn templates

## To deploy these stacks

```bash
aws cloudformation create-stack --stack-name=credentials --template-body file://stage01-credentials.yaml --parameters ParameterKey=ConsumerKey,ParameterValue=$TWITTER_CONSUMER_KEY ParameterKey=ConsumerSecret,ParameterValue=$TWITTER_CONSUMER_SECRET ParameterKey=AccessToken,ParameterValue=$TWITTER_ACCESS_TOKEN ParameterKey=AccessTokenSecret,ParameterValue=$TWITTER_ACCESS_TOKEN_SECRET
aws cloudformation create-stack --stack-name=vpc --template-body file://stage02-vpc.yaml
aws cloudformation create-stack --stack-name=buckets --template-body file://stage03-buckets.yaml
aws cloudformation create-stack --stack-name=kinesis --template-body file://stage04-kinesis.yaml --capabilities CAPABILITY_NAMED_IAM
aws cloudformation create-stack --stack-name=producers --template-body file://stage05-producer.yaml --capabilities CAPABILITY_NAMED_IAM

```
