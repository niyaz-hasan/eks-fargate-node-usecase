output "namespace_depends_on" {
  value = kubernetes_namespace.fargate_namespace
}

output "namespace" {
  value = kubernetes_namespace.fargate_namespace.metadata[0].name
}
