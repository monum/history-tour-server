#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { HistoryTourServerStack } from '../lib/history-tour-server-stack';

const app = new cdk.App();
new HistoryTourServerStack(app, 'HistoryTourServerTestStack');
