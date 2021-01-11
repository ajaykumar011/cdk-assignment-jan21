#!/usr/bin/env python3

from aws_cdk import core

from codepipeline_to_ecr.codepipeline_to_ecr_stack import CodepipelineToEcrStack


app = core.App()
CodepipelineToEcrStack(app, "codepipeline-to-ecr")

app.synth()
