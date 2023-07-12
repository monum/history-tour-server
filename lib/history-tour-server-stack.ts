import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {aws_s3 as s3} from 'aws-cdk-lib';
import { aws_dynamodb as dynamodb } from 'aws-cdk-lib';
import { aws_apigateway as apigateway } from 'aws-cdk-lib';

export class HistoryTourServerStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    //create s3 buckets
    new s3.Bucket(this, 'TourAssetsBucket', {
      versioned: true,

    });
    
    new s3.Bucket(this, 'UnapprovedStoryAssetsBucket', {
      versioned: true,

    });

    // create dynamodb tables
    new dynamodb.Table(this, 'RouteTable', {
      partitionKey: { name: 'routeName', type: dynamodb.AttributeType.STRING }
    });

    new dynamodb.Table(this, 'ApprovedUserStoryTable', {
      partitionKey: { name: 'uniqueIdentifier', type: dynamodb.AttributeType.STRING }
    });

    new dynamodb.Table(this, 'UnapprovedUserStoryTable', {
      partitionKey: { name: 'uniqueIdentifier', type: dynamodb.AttributeType.STRING }
    });

    // create endpoint with api gateway
    const api = new apigateway.RestApi(this, 'history-tour-main-api', {
      description: 'API endpoint for history-tour main application.',
      defaultCorsPreflightOptions: { 
        allowOrigins: apigateway.Cors.ALL_ORIGINS } //TODO:update
    });

    //


  }
}
