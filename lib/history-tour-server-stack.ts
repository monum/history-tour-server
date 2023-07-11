import { Duration, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import {aws_s3 as s3} from 'aws-cdk-lib';
import { aws_dynamodb as dynamodb } from 'aws-cdk-lib';

export class HistoryTourServerStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new s3.Bucket(this, 'TourAssetsBucket', {
      versioned: true,

    });
    
    new s3.Bucket(this, 'UnapprovedStoryAssetsBucket', {
      versioned: true,

    });

    new dynamodb.Table(this, 'RouteTable', {
      partitionKey: { name: 'routeName', type: dynamodb.AttributeType.STRING }
    });

    new dynamodb.Table(this, 'ApprovedUserStoryTable', {
      partitionKey: { name: 'uniqueIdentifier', type: dynamodb.AttributeType.STRING }
    });

    new dynamodb.Table(this, 'UnapprovedUserStoryTable', {
      partitionKey: { name: 'uniqueIdentifier', type: dynamodb.AttributeType.STRING }
    });
    
  }
}
