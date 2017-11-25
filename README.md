[]{#AWS_Solution .anchor}**AWS Find Missing Persons by Scanning Social
Media with Amazon Rekognition Workshop **

In this workshop, we'll build a solution that automatically launches and
configures [Amazon Rekognition](https://aws.amazon.com/rekognition/),
[[Amazon Kinesis
Firehose]{.underline}](https://aws.amazon.com/kinesis/firehose/),
[Amazon Simple Storage
Service(S3)](https://aws.amazon.com/s3/?nc2=h_l3_sc), [AWS
Lambda](https://aws.amazon.com/lambda/?nc2=h_l3_c), [Amazon
DynamoDB](https://aws.amazon.com/dynamodb/?nc2=h_l3_db), [Amazon Simple
Notification Service (SNS)](https://aws.amazon.com/sns/), & [Amazon
Elastic Cloud Compute (EC2)](https://aws.amazon.com/ec2/) to collect,
store, process, and analyze data to search for missing persons on social
media data streams. The diagram below presents the Find Missing Persons
by Scanning Social Media with Amazon Rekognition architecture you can
deploy in minutes using this guide and accompanying [AWS
CloudFormation](https://aws.amazon.com/cloudformation/?nc2=h_l3_dm)
template.

![](media/image1.png){width="5.56880249343832in" height="3.15625in"}

1.  This solution uses python code on an EC2 instance to listen to
    Twitter feed to capture images from that feed.

2.  The EC2 instance pushes image metadata in JSON form to S3 via an
    Amazon Kinesis Firehose. 

3.  A Lambda function is invoked based on PUT operation to the initial
    S3 bucket that launches Rekognition API to analyze the photo and
    store the data in a result S3 bucket & DynamoDB

4.  A second Lambda function fires based on PUT operation to the result
    S3 bucket this fires a SNS message to monitoring users

5.  If you choose to persist raw data, AWS Lambda decodes the data and
    puts it into Amazon Kinesis Firehose which delivers it to Amazon S3.
     

**What you\'ll accomplish:**

> **Deploy Find Missing Persons by Scanning Social Media with Amazon
> Rekognition** using [AWS
> CloudFormation](https://aws.amazon.com/cloudformation/). The
> CloudFormation template will automatically launch and configure the
> components necessary to consume and analyze streaming data.
>
> **Automatically analyze streaming data** in an Amazon Kinesis
> Analytics application. You can customize the Amazon Kinesis Analytics
> application that is included with the solution.

**What you\'ll need before starting:**

1.  **An AWS account: **You will need an AWS account to begin
    provisioning resources. [Sign up for
    AWS](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html).

2.  **Twitter Developer account and create a Twitter application with
    keys and tokens** <https://apps.twitter.com>

3.  **Create SSH Key pair** unless you already have one you can use for
    this workshop

> **Skill level:** This solution is intended for IT infrastructure
> professionals who have practical experience with streaming data and
> architecting on the AWS Cloud.

**What We\'ll Cover**

The procedure for deploying this architecture on AWS consists of the
following steps. For detailed instructions, follow the links for each
step.

Step 1. Pre-Workshop Setup Steps 
=================================

1.  Set up your Twitter Application (Required step)

    a.  Goto <https://apps.twitter.com>

        ![](media/image2.png){width="4.7575393700787405in"
        height="3.185416666666667in"}

    b.  Login if you have an account, otherwise sign up for a new
        account. Note you will need your mobile number included in your
        account profile to build Twitter apps.

> ![](media/image3.png){width="4.763552055993001in"
> height="3.2576388888888888in"}

a.  Select Create New App

    ![](media/image4.png){width="4.756944444444445in"
    height="3.3354516622922135in"}

b.  Provide a unique name such as FindMissingPersonsRekognitions & add
    your initials etc

    ![](media/image5.png){width="4.778502843394576in"
    height="3.8749660979877514in"}

c.  Next you'll get the details from your new app. Key data points to
    collect are consumer key/api highlighted by the red arrow below.

    ![](media/image6.png){width="4.802083333333333in" height="3.8125in"}

d.  Click on the Key & Access tokens tab

    ![](media/image7.png){width="4.71875in"
    height="4.510295275590551in"}

e.  To generate tokens -- click on the create my access token then
    capture the details such as shown in the screen below

    ![](media/image8.png){width="4.703301618547681in"
    height="3.90625in"}

f.  Capture your API Key & Secret and Access Token and Secret for later
    use in Notepad or text editor

<!-- -->

1.  Create a new EC2 Key Pair - For this workshop, you will need to
    create an EC2 instance using an SSH keypair. ***[If you already have
    a SSH key pair in Ireland region Please skip this section and go
    onto the next.]{.underline}*** The following steps outline creating
    a unique SSH keypair for you to use in this workshop.

    a.  Sign into the AWS Management Console and open the Amazon EC2
        console at https://console.aws.amazon.com/ec2.

    b.  In the upper-right corner of the AWS Management Console, confirm
        you are in the desired AWS region (e.g., Ireland).

    c.  Click or type EC2 on search line then click on EC2 service from
        the menu.

    d.  e.  Click on Key Pairs in the NETWORK & SECURITY section near
        the bottom of the leftmost menu. This will display a page to
        manage your SSH key pairs.

        ![](media/image9.emf){width="4.961605424321959in"
        height="3.6486111111111112in"}

    f.  To create a new SSH key pair, click the Create Key Pair button
        at the top of the browser window

        ![](media/image10.emf){width="4.979166666666667in"
        height="1.4789818460192476in"}

    g.  In the resulting pop up window, type \[First Name\]-\[Last
        Name\]-Rekognition into the Key Pair Name: text box and click
        Create.

        ![](media/image11.emf){width="3.7291666666666665in"
        height="1.4078805774278216in"}

    h.  The page will download the file "\[Your-Name\]-Rekognition.pem"
        to the local drive. Follow the browser instructions to save the
        file to the default download location.

    i.  Remember the full path to the file .pem file you just
        downloaded. You will use the Key Pair you just created to manage
        your EC2 instances for the rest of the lab

Step 2 Launch the Stack
=======================

This automated AWS CloudFormation template deploys Find Missing Persons
by Scanning Social Media with Amazon Rekognition on the AWS Cloud.
Please make sure that you've configured IAM roles before launching the
template.

Note

You are responsible for the cost of the AWS services used while running
this solution. We are providing \$25 AWS credit which should more than
cover those cost during the workshop.

1.  Log in to the AWS Management Console and click the button below to
    launch the rekognition-workshop AWS CloudFormation template.

> ![ Streaming Analytics Pipeline launch button
> ](media/image12.png){width="1.125in" height="0.6875in"}
>
> You can also [download the
> template](https://s3-eu-west-1.amazonaws.com/awsreinvent2017workshop/RekognitionWorkshopCFN.json)
> as a starting point for your own implementation.

1.  Be sure to launch the template in the EU (Ireland) Region
    (eu-west-1).

2.  On the **Select Template** page, verify that you selected the
    correct template and choose **Next**.

> ![](media/image13.png){width="5.363875765529309in" height="4.46875in"}

1.  On the **Specify Details** page, assign a name to your Find Missing
    Persons by Scanning Social Media with Amazon Rekognition solution
    stack. This stack name should be all lower case characters & numbers
    and be short since we use it for bucket names etc.

2.  Under **Parameters**, review the parameters for the template, and
    modify them as necessary. This solution uses the following default
    values.

  **Parameter**           **Default**            **Description**
  ----------------------- ---------------------- ---------------------------------------------------------------------------------------------------------------------------
  **StackName**           twtrrekog              Name of the Stack to launch
  EmailAddress            *\<Requires input\>*   Email address to use during workshop so you can receive emails notifications.
  InstanceType            *T2.Micro*             Select your instance type. Recommend T2.Micro
  KeyName                 *\<Requires input\>*   SSH key for Ireland region to use during the workshop. Without this key you will not be able to connect to your instance.
  SSHLocation             *0.0.0.0/0*            The IP address range that can be used to SSH to the EC2 instances
  TwitterConsumerKey      *\<Requires input\>*   Twitter Consumer Key, as generated by dev.twitter.com. Part of the pre setup steps
  TwitterConsumerSecret   *\<Requires input\>*   Twitter Consumer Secret, as generated by dev.twitter.com Part of the pre setup steps
  **TwitterToken**        *\<Requires input\>*   Twitter Access Token, as generated by dev.twitter.com. Part of the pre setup steps
  TwitterTokenSecret      *\<Requires input\>*   Twitter Access Token Secret, as generated by dev.twitter.com Part of the pre setup steps

> It should look something like the picture below
>
> ![](media/image14.png){width="5.348877952755905in"
> height="3.8722222222222222in"}

1.  Verify that you modified the correct parameters for your chosen
    destination.

2.  Choose **Next**.

3.  On the **Options** page, choose **Next**.

> ![](media/image15.png){width="5.612272528433945in"
> height="4.675694444444445in"}

1.  On the **Review** page, review and confirm the settings. Be sure to
    check the box acknowledging that the template will create AWS
    Identity and Access Management (IAM) resources.

> ![](media/image16.png){width="5.587265966754155in"
> height="4.654861111111111in"}

1.  Choose **Create** to deploy the stack.

> You can view the status of the stack in the AWS CloudFormation console
> in the Status column. You should see a status of **CREATE\_COMPLETE**
> in roughly five (5) minutes.

Step 3. Validate and Start the Application
==========================================

Once the stack is created, complete the following steps.

1.  Navigate to the stack **Outputs** tab.

2.  Note the name of the EC2 Instance and capture the Public IP address

3.  Open SSH connection to your instance (if using windows you'll need
    putty & puttygen to connect)

4.  Goto /home/ec2-user/rekognition-workshop directory

5.  Run "aws configure" to populate aws credentials on to the EC2
    instance.

  **Parameter**           **Default**                            **Description**
  ----------------------- -------------------------------------- ---------------------------------------------------------------
  AWS Access Key ID       \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*A5ZA   Access key to IAM user, retrieved from the IAM Console
  AWS Secret Access Key   \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*8fwG   Secret Access key to IAM user, retrieved from the IAM Console
  Default region name     *eu-west-1*                            Region setting
  Default output format   *table*                                Format of output results in the AWS CLI

 

\[ec2-user@ip-172-31-2-51 rekognition-workshop\]\$ aws configure

AWS Access Key ID \[\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*A5ZA\]:

AWS Secret Access Key \[\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*8fwG\]:

Default region name \[eu-west-1\]:

Default output format \[table\]:

1.  Run the python source code to start streaming twitter data. Monitor
    the KFH delivery stream to see feeds stored in destination bucket.

> \[ec2-user@ip-172-31-2-51 rekognition-workshop\]\$ python
> twitter\_streaming.py

Step 4. Start Twitter Streaming Data
====================================

Now that you have all the infrastructure set up and verified let's start
the Twitter feed and run the application to search for missing persons.

1.  First step

2.  Second Step

3.  

Step 5. Clean up 
=================

Once complete with the workshop to clean up the environment goto
Cloudformation and delete the rekognition-workshop stack by placing a
check mark by it and selecting the delete action. This will remove the
resources created in the workshop.
