import boto3
from prettytable import PrettyTable

all_regions_list = []
aws_profile = 'AWS_PROFILE'
final_table = PrettyTable()
final_table.field_names = ["Secret_Name", "Region"]

session = boto3.Session(profile_name=aws_profile)
ec2_client = session.client('ec2',region_name='us-east-1')
regions = ec2_client.describe_regions()

def all_regions(regions):
    for region in list(regions.items())[0][1]:
        all_regions_list.append(region['RegionName'])
    return(all_regions_list)

def collect_secrets(all_regions_list):
    for region in all_regions_list:
        session = boto3.Session(profile_name=aws_profile, region_name=region)
        ec2_client = session.client('secretsmanager')
        response = ec2_client.list_secrets()
        print('Check secrets in the region')
        print(region)
        if len(response['SecretList']) !=0:
            session = boto3.Session(profile_name=aws_profile, region_name=region)
            ec2_client = session.client('secretsmanager')
            response = ec2_client.list_secrets()
            results = response["SecretList"]

            while "NextToken" in response:
                response = ec2_client.list_secrets(NextToken=response["NextToken"])
                for secret in response['SecretList']:
                    if 'whitelist' in secret['Name']:
                        final_table.add_row([secret['Name'], region])
    print(final_table)

def main():
    rgions_list = all_regions(regions)
    secrets_list = collect_secrets(all_regions_list)

if __name__ == "__main__":
    main()
