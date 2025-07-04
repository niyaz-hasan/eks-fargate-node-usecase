resource "aws_db_subnet_group" "subnet_group" {
  name       = "aurora-subnet-group"
  subnet_ids = var.private_subnets
}

resource "aws_rds_cluster" "aurora_mysql" {
  cluster_identifier           = "aurora-mysql-cluster"
  engine                       = "aurora-mysql"
  engine_version               = "8.0.mysql_aurora.3.04.0"
  database_name                = var.database_name

  db_subnet_group_name         = aws_db_subnet_group.subnet_group.name
  vpc_security_group_ids       = var.rds_security_group_ids

  manage_master_user_password  = true
  master_username              = var.db_username
  skip_final_snapshot          = true
}



resource "aws_rds_cluster_instance" "aurora_instances" {
  count                     = 1
  identifier                = "aurora-instance-${count.index}"
  cluster_identifier        = aws_rds_cluster.aurora_mysql.id
  instance_class            = "db.t3.medium"
  engine                    = aws_rds_cluster.aurora_mysql.engine
  db_subnet_group_name      = aws_db_subnet_group.subnet_group.name
  publicly_accessible       = false
  
}

output "aurora_cluster_endpoint" {
  value = aws_rds_cluster.aurora_mysql.endpoint
}

#output "aurora_cluster_instance_endpoint" {
#  value = aws_rds_cluster.aurora_instances.endpoint
#}