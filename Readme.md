This is a personal assignment code repo
Readme file is not specific to any code or project. This is a general reference for evualation


*As this is development mode, some hard-coded values are included, which would be removed soon.
*


Q- CodeBuild2ECR - Setup Infra for pushing code to codecommit and it is build and Artifact is pushed to ECR. In this example we are using buidspec in the program


Q1- 
Assignment 1: Application LoadBalancer and Instance setup
Write the CDK script to deploy the application behind load balancer. The
resource to be created are below:
A) Two EC2 Windows instances  (Windows is created from ASG for best practice)
B) ALB with two listener on port 443 and 4780 both HTTPS protocol
C) Two Target groups on the above port. Each target group should have one
instance.
D) The listener should be configured with Weighted Rule - have 100% traffic
on one of the target group.
E) Consider the SG for all the application resources

Assignment 2: Network LoadBalancer and Instance setup
Write the CDK script to deploy the application behind the network load
balancer. The resource to be created are below:
A) Two EC2 Windows instances
B) NLB with two listener on port 443 and 4780 both TCP protocol
C) Two Target groups on the above port. Each target group should have one
instance.
D) The listener should be configured 
on one of the target group.
E) Consider the SG for all the application resources

Assignment 4: RDS Automation
Write the CDK script to create RDS instance as Master slave with multi AZ.
Assignment 5: Active MQ Automation
Write the CDK script to create Active MQ instance with multi AZ.

Assignment 7: EFS Automation (This is not tested)
Write the CDK script to do the following:
A) Create a EFS file share system as multi AZ
B) Launch an EC2 Linux Instance
C) Mount the EFS to this instance
D) Create folder structure as per the provided configuration:
E) You can take the below folder structure to start with:
MainFolder:
ApplicationFolder:
Application1:
Code:
Artifacts:
Application2:
Code:
Artifacts:
LogsFolder:
DatabaseFolder
F) Define the backup policy and automate the same
