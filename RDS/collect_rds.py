# importing required libraries
import boto3
from prettytable import PrettyTable

session = boto3.Session(profile_name='default')

ec2_client = session.client('ec2')
regions = ec2_client.describe_regions()

final_table = PrettyTable()
final_table.field_names = ["Database_Name", "Backup_Retention_Period", "Availability_Zone", "DeletionProtection", "Terraform"]

all_regions_list = []

def all_regions(regions):
    for region in list(regions.items())[0][1]:
        all_regions_list.append(region['RegionName'])
    return(all_regions_list)

def collect_rds(all_regions_list):
    for region in all_regions_list:
        print("Checking region is:",region)
        rds_client = session.client('rds', region_name=region)
        response = rds_client.describe_db_instances()
        list_response = list(response.items())[0][1]
        for rds in list_response:
            if rds['TagList']:
                if any(d['Key'] == 'terraform' for d in rds['TagList']):
                    for tag in rds['TagList']:
                        if tag['Key'] == 'terraform':
                            final_table.add_row([rds['DBInstanceIdentifier'], rds['BackupRetentionPeriod'], rds['AvailabilityZone'],rds['DeletionProtection'], tag['Value']])
                else:
                    final_table.add_row([rds['DBInstanceIdentifier'], rds['BackupRetentionPeriod'], rds['AvailabilityZone'], rds['DeletionProtection'], ''])
            else:
                final_table.add_row([rds['DBInstanceIdentifier'], rds['BackupRetentionPeriod'], rds['AvailabilityZone'], rds['DeletionProtection'], ''])
    print(final_table)

def main():
    rgions_list = all_regions(regions)
    rds_list = collect_rds(all_regions_list)

if __name__ == "__main__":
    main()
