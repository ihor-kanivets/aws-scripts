db_list=(
)
retention_period=7
for each in "${db_list[@]}"
do
  echo "Modifying $each RDS"
  aws rds modify-db-instance --db-instance-identifier $each --backup-retention-period $retention_period --deletion-protection --apply-immediately > /dev/null
done
