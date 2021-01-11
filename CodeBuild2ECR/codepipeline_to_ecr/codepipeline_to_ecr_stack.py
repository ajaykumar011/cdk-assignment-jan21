from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_ecr as _ecr
from aws_cdk.aws_ecr_assets import DockerImageAsset
from aws_cdk import aws_iam as iam
from os import path


class CodepipelineToEcrStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        #print(self.node.try_get_context('global')['codecommit_repo'])
        this_dir = path.dirname(__file__)
        repo = codecommit.Repository(self, "Repo", repository_name=self.node.try_get_context('global')['codecommit_repo'])
        #repo.on_commit("CommitToMaster", target=targets.CodeBuildProject(project), branches=["master"])
        repo.notify(self.node.try_get_context('global')['sns_topic_arn'])
        source_artifact = codepipeline.Artifact()

        ecr = _ecr.Repository(self, "MyArtifactECR", repository_name=self.node.try_get_context('global')['ecr_repo'])
        #asset = DockerImageAsset(self, "MyBuildImage", directory=path.join(this_dir)


        # #iam_role =  iam.Role.add_managed_policy("AmazonEC2ContainerRegistryFullAccess")
        # ecr_policy = iam.ManagedPolicy(self, "policy", managed_policy_name="AmazonEC2ContainerRegistryFullAccess")
        # cb_role =  iam.Role.add_managed_policy(self, policy=ecr_policy)

        # role1 = iam.Role.import(this, "service-role", {
        #   roleArn: "arn:aws:iam::143787628822:role/CodeBuildServiceRole" ,
        # });

        cb_role = iam.Role.from_role_arn(self, "service-role", role_arn="arn:aws:iam::143787628822:role/codepipeline-to-ecr-DockerBuildRole2BAC6ED2-16RU4CVCJYR5D") 
       
        cb_docker_build = codebuild.PipelineProject(
            self, "DockerBuild",
            project_name=self.node.try_get_context('global')['codebuild_name'],
            #build_spec=codebuild.BuildSpec.from_source_filename(filename='./buildspec.yml'),
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "build": {
                        #"commands": ["echo \"Hello, CodeBuild!\"","$(aws ecr get-login --no-include-email --region $AWS_DEFAULT_REGION)","docker build -t ${image_name}:latest .","docker push ${image_name}:latest"
                        "commands": ["aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 143787628822.dkr.ecr.us-east-1.amazonaws.com","docker build -t cloudzone-ecrrepo .","docker tag cloudzone-ecrrepo:latest 143787628822.dkr.ecr.us-east-1.amazonaws.com/cloudzone-ecrrepo:latest","docker push 143787628822.dkr.ecr.us-east-1.amazonaws.com/cloudzone-ecrrepo:latest"
                        ]
                    }
                }
            }),
            role=cb_role,
            environment=codebuild.BuildEnvironment(privileged=True, build_image=codebuild.LinuxBuildImage.STANDARD_2_0),
            # pass the ecr repo uri into the codebuild project so codebuild knows where to push
            environment_variables={
                'ecr_uri': codebuild.BuildEnvironmentVariable(value=ecr.repository_uri),
                'image_name': codebuild.BuildEnvironmentVariable(value=self.node.try_get_context('global')['ecr_image'])
            },
            description='Pipeline for CodeBuild',
            timeout=core.Duration.minutes(20)
        )
        
        pipeline = codepipeline.Pipeline(
            self, "Pipeline",
            pipeline_name=self.node.try_get_context('global')['pipeline'],
            stages=[
                    codepipeline.StageProps(
                    stage_name='Source',
                    actions=[
                            codepipeline_actions.CodeCommitSourceAction(
                            action_name='CodeCommit',
                            repository=repo,
                            run_order=1,
                            output=source_artifact,
                            trigger=codepipeline_actions.CodeCommitTrigger.EVENTS
                        ),
                    ]
                ),
                    codepipeline.StageProps(
                    stage_name='Build',
                    actions=[
                            codepipeline_actions.CodeBuildAction(
                            action_name='DockerBuildImages',
                            input=source_artifact,
                            project=cb_docker_build,   
                            run_order=1,
                            #role=cb_role
                        )
                    ]
                )
            ]

        )
        # pipeline = codepipeline.Pipeline(self, "MyPipeline",
        #     pipeline_name="MyPipeline"
        # )
        # source_output = codepipeline.Artifact()
        # source_action = codepipeline_actions.CodeCommitSourceAction(
        #     action_name="CodeCommit",
        #     repository=repo,
        #     output=source_output
        # )
        # pipeline.add_stage(
        #     stage_name="Source",
        #     actions=[source_action]
        # )

        # pipeline.add_stage(
        #     stage_name="Build"
        # )
           
