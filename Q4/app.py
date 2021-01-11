#!/usr/bin/env python3

from aws_cdk import core

from vpc_stack.cdk_vpc_stack import CdkVpcStack
from rds_stack.cdk_rds_stack import CdkRdsStack

app = core.App()

vpc_stack = CdkVpcStack(app, "cdk-vpc")
rds_stack = CdkRdsStack(app, "cdk-rds", vpc=vpc_stack.vpc)

# Add a tag to all constructs in the stack

core.Tags.of(vpc_stack).add("Project", (app.node.try_get_context('project')['tag_value']))
core.Tags.of(rds_stack).add("Project", (app.node.try_get_context('project')['tag_value']))

app.synth()