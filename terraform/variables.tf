variable "container_environment_name" {
  description = "The name of the container app environment (k8s)"
  type        = string
  default = "assignment-app-environment"
}

variable "container_app_name" {
  description = "The name of the container app "
  type        = string
  default = "assignment-app"
}

variable "container_image" {
  description = "The Docker image to deploy to the container app"
  type        = string
  default = "oshericko/hometask:test"
}

# The next 2 variables are a bit tricky, you have to use the specifc pair.
# In (CPU, Memory) format:
# The lowest is (0.25,0.5Gi) it adds (0.25,0.5Gi) every step until it reaches the limit which is(4,8Gi).

variable "container_cpu" {
  description = "The CPU allocated to the container"
  type        = number
  default     = 0.25
}

variable "container_memory" {
  description = "The memory allocated to the container"
  type        = string
  default     = "0.5Gi"
}

variable "admin_password" {
  description = "The password for the SQL Server administrator"
}
