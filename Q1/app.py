#!/usr/bin/env python3

from aws_cdk import core

from vpc_stack.cdk_vpc_stack import CdkVpcStack
from ec2_stack.cdk_ec2_stack import CdkEc2Stack


# env_prod =  core.Environment(account="143787628822", region="us-east-1")
# env_dev = core.Environment(account="143787628822", region="us-east-2")

props = {'namespace':'cloudzone-stack'}

app = core.App()

vpc_stack = CdkVpcStack(app, "cdk-vpc")
ec2_stack = CdkEc2Stack(app, "cdk-ec2", vpc=vpc_stack.vpc)

# Add a tag to all constructs in the stack
core.Tags.of(vpc_stack).add("Project","Cloudzone-vpc")
core.Tags.of(ec2_stack).add("Project","Cloudzone-Instance")

app.synth()
