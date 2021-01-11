from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_route53 as route53
import aws_cdk.aws_elasticloadbalancingv2_targets as elbtarget



class CdkEc2Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        arn = (self.node.try_get_context('project')['cert_arn'])  #arn
        ec2_type = (self.node.try_get_context('project')['ec2_type']) #ec2_type
        key_name = (self.node.try_get_context('project')['key_name']) #key_name 

        certificate = acm.Certificate.from_certificate_arn(self, "Certificate", arn)

        #Windows AMI       
        windows_ami = ec2.MachineImage.latest_windows(ec2.WindowsVersion.WINDOWS_SERVER_2019_ENGLISH_FULL_BASE)
        
        #Reading Userdata from file to install IIS from userdata.ps1
        with open("./user_data/user_data.ps1") as f:
            user_data = f.read()
        
        #EC2 SG
        ec2_security_group = ec2.SecurityGroup(self, "SecurityGroup",
            vpc=vpc,
            description="Allow RDP access to ec2 instances",
            allow_all_outbound=True
        )
        ec2_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(3389), "allow RDP access from the world")
        ec2_security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow port 80")

        # Create Instance from ASG with ALB

        alb = elb.ApplicationLoadBalancer(self, "myALB", vpc=vpc, internet_facing=True)
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(443), "Internet access ALB 443")
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(4780), "Internet access ALB 4780")
       
        # Create Autoscaling Group with one EC2 hosts
        asg1 = autoscaling.AutoScalingGroup(self, "myASG1",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=windows_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                )
        asg2 = autoscaling.AutoScalingGroup(self, "myASG2",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=windows_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=1,
                                                )

        #2 Target Group
        tg1 = elb.ApplicationTargetGroup(self, "TGroup1", vpc=vpc, port=80, targets=[asg1])
        tg2 = elb.ApplicationTargetGroup(self, "TGroup2", vpc=vpc, port=80, targets=[asg2])
    
        # 2 Listeners       
        listener1 = alb.add_listener("Listener1", port=443, protocol=elb.ApplicationProtocol.HTTPS, open=True, certificates=[certificate])
        
        wtg = elb.WeightedTargetGroup(target_group=tg1, weight=2)
        listener1.add_action("Weighted", action=elb.ListenerAction.weighted_forward([wtg]))
        listener2 = alb.add_listener("Listener2", port=4780, protocol=elb.ApplicationProtocol.HTTPS, open=True, certificates=[certificate], default_target_groups=[tg2])
       
        #Output
        core.CfnOutput(self, "ALB-DNSName", value=alb.load_balancer_dns_name)

