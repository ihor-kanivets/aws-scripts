import boto3
from prettytable import PrettyTable

all_regions_list = []
aws_profile = 'AWS_PROFILE'
final_table = PrettyTable()
final_table.field_names = ["Secret_name", "Lambda", "Region"]

session = boto3.Session(profile_name=aws_profile)
ec2_client = session.client('ec2',region_name='us-east-1')
regions = ec2_client.describe_regions()

def all_regions(regions):
    for region in list(regions.items())[0][1]:
        all_regions_list.append(region['RegionName'])
    return(all_regions_list)

def collect_lambdas(all_regions_list):
    for region in all_regions_list:
        print('Checking region:')
        print(region)
        session = boto3.Session(profile_name=aws_profile,region_name=region)
        lambda_client = session.client('lambda')
        response = lambda_client.list_functions()

        paginator = lambda_client.get_paginator('list_functions')
        if len(response['Functions']) !=0:
            for response in paginator.paginate():
                for function in response['Functions']:
                    if 'Environment' in function.keys():
                        for secret_name in function['Environment']['Variables'].values():
                            if 'SEARCH_WORD' in secret_name:
                                final_table.add_row([secret_name, function['FunctionName'], region])
    print(final_table)

def main():
    regions_list = all_regions(regions)
    lambdas_list = collect_lambdas(all_regions_list)

if __name__ == "__main__":
    main()
