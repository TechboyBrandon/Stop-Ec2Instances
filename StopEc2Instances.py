import boto3

def lambda_handler(event, context):
    # Initialize EC2 client
    ec2_client = boto3.client(service_name="ec2", region_name="us-east-1")
    
    # Retrieve the instances
    response = ec2_client.describe_instances()
    
    ID = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] == 'running':
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'env' and tag['Value'] == 'test':
                        server = instance['InstanceId']
                        ID.append(server)
    
    # Filter EC2 instances by tag
    filter_ec2 = {"Name": "tag:env", "Values": ["test"]}
    
    ec2_resource = boto3.resource(service_name="ec2", region_name="us-east-1")
    for each in ec2_resource.instances.filter(Filters=[filter_ec2]):
        print(each.id)
        each.stop()  # Correct method call
    
    print("List of EC2 servers that will be stopped are: " + str(ID))
    
    # Stop instances using client
    if ID:  # Check if the list is not empty
        response = ec2_client.stop_instances(InstanceIds=ID)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Stopped {len(ID)} instances')
    }
