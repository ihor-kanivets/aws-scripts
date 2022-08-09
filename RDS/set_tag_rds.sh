db_list=(
)
for each in "${db_list[@]}"
do
  echo "Tagging $each RDS"
  rds_arn=$(aws rds describe-db-instances --db-instance-identifier $each --query 'DBInstances[].DBInstanceArn' | awk -F '"' '{print $2}')
  aws rds add-tags-to-resource --resource-name $rds_arn \
      --tags "[{\"Key\": \"terraform\",\"Value\": \"false\"}]"
done
