from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class CdkRdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_mysql = rds.DatabaseInstance(self, "MySQL_DB1",
                                             engine=rds.DatabaseInstanceEngine.mysql(
                                                 version=rds.MysqlEngineVersion.VER_5_7_30
                                             ),
                                             instance_type=ec2.InstanceType.of(
                                                 ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
                                             vpc=vpc,
                                             vpc_subnets=ec2.SubnetType.PRIVATE,
                                             #publicly_accessible=True,
                                             port=3306,
                                             multi_az=True,
                                             allocated_storage=100,
                                             storage_type=rds.StorageType.GP2,
                                             cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
                                             deletion_protection=False,
                                             removal_policy=core.RemovalPolicy.DESTROY,
                                             delete_automated_backups=True,
                                             backup_retention=core.Duration.days(3),
                                             parameter_group=rds.ParameterGroup.from_parameter_group_name(
                                                 self, "para-group-mysql",
                                                 parameter_group_name="default.mysql5.7"
                                             )
                                             )
 
        db_slave = rds.DatabaseInstanceReadReplica(self, "ReadReplica", source_database_instance=db_mysql,
                        instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
                        vpc=vpc)
        
        db_mysql.connections.allow_default_port_from_any_ipv4()
        
        #output 
        core.CfnOutput(self, "RDSEndpoint", value=db_mysql.db_instance_endpoint_address)
        core.CfnOutput(self, "RDSPort", value=db_mysql.db_instance_endpoint_port)
        core.CfnOutput(self, "RDSEngineFamily", value=db_mysql.engine.engine_family)
        core.CfnOutput(self, "RDSEngineType", value=db_mysql.engine.engine_type)
        core.CfnOutput(self, "RDSEngineVersion", value=db_mysql.engine.engine_version.full_version)
        core.CfnOutput(self, "RDSIdentifier", value=db_mysql.instance_identifier)

