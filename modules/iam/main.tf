############################################## IAM Role for EKS Cluster ################################################
resource "aws_iam_role" "eks_role" {
  name = "eksClusterRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "eks.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  role       = aws_iam_role.eks_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

######################################## IAM Role for EKS Node Group #####################################################
resource "aws_iam_role" "eks_node_role" {
  name = "eksNodeGroupRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Service = "ec2.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_worker_node_policy" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
}

resource "aws_iam_role_policy_attachment" "eks_cni_policy" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
}

resource "aws_iam_role_policy_attachment" "ecr_read_only" {
  role       = aws_iam_role.eks_node_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

####################################### IAM Role for EKS Fargate Profile ########################################################
resource "aws_iam_role" "fargate_profile_role" {
  name = "${var.name}-eks-fargate-profile-role-apps"

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "eks-fargate-pods.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

# IAM Policy Attachment to IAM Role
resource "aws_iam_role_policy_attachment" "eks_fargate_pod_execution_role_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSFargatePodExecutionRolePolicy"
  role       = aws_iam_role.fargate_profile_role.name
}

### Datasource: AWS Load Balancer Controller IAM Policy get from aws-load-balancer-controller/ GIT Repo (latest)
data "http" "lbc_iam_policy" {
  url = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/install/iam_policy.json"

  # Optional request headers
  request_headers = {
    Accept = "application/json"
  }
}

output "lbc_iam_policy" {
  #value = data.http.lbc_iam_policy.body
  value = data.http.lbc_iam_policy.response_body
}

########################################## Create AWS Load Balancer Controller IAM Policy ################################################
resource "aws_iam_policy" "lbc_iam_policy" {
  name        = "${var.name}-AWSLoadBalancerControllerIAMPolicy"
  path        = "/"
  description = "AWS Load Balancer Controller IAM Policy"
  policy = data.http.lbc_iam_policy.response_body
}

output "lbc_iam_policy_arn" {
  value = aws_iam_policy.lbc_iam_policy.arn 
}

############################  Create IAM Role #############################################
resource "aws_iam_role" "lbc_iam_role" {
  name = "${var.name}-lbc-iam-role"

  # Terraform's "jsonencode" function converts a Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRoleWithWebIdentity"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Federated = "${var.aws_iam_openid_connect_provider_arn}"
        }
        Condition = {
          StringEquals = {
            "${var.aws_iam_openid_connect_provider_extract_from_arn}:aud": "sts.amazonaws.com",            
            "${var.aws_iam_openid_connect_provider_extract_from_arn}:sub": "system:serviceaccount:kube-system:aws-load-balancer-controller"
          }
        }        
      },
    ]
  })

  tags = {
    tag-key = "AWSLoadBalancerControllerIAMPolicy"
  }
}

# Associate Load Balanacer Controller IAM Policy to  IAM Role
resource "aws_iam_role_policy_attachment" "lbc_iam_role_policy_attach" {
  policy_arn = aws_iam_policy.lbc_iam_policy.arn 
  role       = aws_iam_role.lbc_iam_role.name
}


######################  IRSA Flask backend retrieve secrets from AWS Secrets Manager ###########################################################
resource "aws_iam_role" "flask_irsa" {
  name = "eks-irsa-flask-backend"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Principal = {
        Federated = "${var.aws_iam_openid_connect_provider_arn}"
      },
      Action = "sts:AssumeRoleWithWebIdentity",
      Condition = {
        StringEquals = {
          "${var.aws_iam_openid_connect_provider_extract_from_arn}:aud": "sts.amazonaws.com",            
          "${var.aws_iam_openid_connect_provider_extract_from_arn}:sub": "system:serviceaccount:backend:flask-sa"
        }
      }
    }]
  })
}

resource "aws_iam_role_policy" "flask_secret_access" {
  name = "flask-secretsmanager-policy"
  role = aws_iam_role.flask_irsa.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect = "Allow",
      Action = [
        "secretsmanager:GetSecretValue"
      ],
      Resource = "*"
    }]
  })
}

############################################## outputs #####################################################################
output "lbc_iam_role_arn" {
  description = "AWS Load Balancer Controller IAM Role ARN"
  value = aws_iam_role.lbc_iam_role.arn
}


output "eks_cluster_role_arn" {
    value = aws_iam_role.eks_role.arn
}

output "eks_node_role_arn" {
    value = aws_iam_role.eks_node_role.arn
}


output "fargate_profile_role_arn" {
    value = aws_iam_role.fargate_profile_role.arn
}

output "eks_role_depends_on" {
  value = aws_iam_role.eks_role
}

output "lbc_iam_depends_on" {
  value = aws_iam_role.lbc_iam_role
}