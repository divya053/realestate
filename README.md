## realestate
#prerequisites
Docker installed and running locally

AWS account with permissions for ECR & EKS
#Step 1: Create an EKS Cluster (if not created)

eksctl create cluster --name my-eks-cluster --region us-east-1 --nodes 2 --node-type t3.medium

#Step 2: Build Docker Images Locally
Navigate to each microservice folder, then:

docker build -t <service_name>:latest .

#Step 3: Create an AWS ECR Repository (if not already created)

aws ecr create-repository --repository-name <service_name> --region <region>

#Step 4: Authenticate Docker to AWS ECR

aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<region>.amazonaws.com

#Step 5: Tag Docker Images for ECR

docker tag <service_name>:latest <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<service_name>:latest

#Step 6: Push Docker Images to ECR

docker push <aws_account_id>.dkr.ecr.<region>.amazonaws.com/<service_name>:latest

#Step 7: Deploy microservice to Kubernetes
Use your Kubernetes deployment YAML files (user-service-deployment.yaml):

kubectl apply -f user-service-deployment.yaml
Check pods:
kubectl get pods

Check services:
kubectl get svc

#Step 8: Enable Horizontal Pod Autoscaling (Optional)

kubectl autoscale deployment user-service --cpu-percent=50 --min=2 --max=5

#Step 9: Access your services

kubectl get svc
