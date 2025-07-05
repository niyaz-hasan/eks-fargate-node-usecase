module "vpc" {
  source = "./modules/vpc"
  name           = var.name
  vpc_cidr_block = var.vpc_cidr_block
  
}

module "iam" {
  source = "./modules/iam"
  name = var.name
  aws_iam_openid_connect_provider_arn = module.eks.aws_iam_openid_connect_provider_arn
  aws_iam_openid_connect_provider_extract_from_arn = module.eks.aws_iam_openid_connect_provider_extract_from_arn

  depends_on = [
    module.vpc
  ]

}

module "ecr" {
  source = "./modules/ecr"
}

module "security_group" {
  source = "./modules/security_group"
  name   = var.name
  vpc_id = module.vpc.vpc_id

  depends_on = [
    module.vpc
  ]
}

module "eks" {
  source = "./modules/eks"
  name                = var.name
  public_subnets      = module.vpc.public_subnets
  private_subnets     = module.vpc.private_subnets
  cluster_role_arn    = module.iam.eks_cluster_role_arn
  node_role_arn       = module.iam.eks_node_role_arn
  fargate_profile_role_arn = module.iam.fargate_profile_role_arn
  eks_oidc_root_ca_thumbprint = var.eks_oidc_root_ca_thumbprint
  cluster_role_dependency = module.iam.eks_role_depends_on
  namespace_depends_on   = module.helm.namespace_depends_on
  namespace           = module.helm.namespace
  security_group_ids  = [module.security_group.eks_security_group_id]

  depends_on = [
    module.iam,
    module.vpc,
    module.security_group
  ]
}

module "helm" {
  source = "./modules/helm"
  cluster_id = module.eks.cluster_id
  cluster_endpoint = module.eks.cluster_endpoint
  cluster_certificate_authority_data = module.eks.cluster_certificate_authority_data
  lbc_iam_depends_on = module.iam.lbc_iam_depends_on
  lbc_iam_role_arn   = module.iam.lbc_iam_role_arn
  vpc_id             = module.vpc.vpc_id
  aws_region         = var.region

  depends_on = [
    module.eks,
    module.iam,
    module.vpc
  ]
}

module "rds" {
  source               = "./modules/rds"
  name                 = var.name
  private_subnets      = module.vpc.private_subnets
  db_username          = var.db_username
  database_name        = var.database_name
  rds_security_group_ids  = [module.security_group.rds_security_group_aurora_id]

  depends_on = [
    module.vpc,
    module.security_group,
    module.eks
  ]
}
