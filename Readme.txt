# Basic K8S and Pulumi

Goal:
    - Create a simple Dockerfile, build it and deploy it on k8s orchestration using pulumi.

Prerequisites:
    -  minikube :  https://minikube.sigs.k8s.io/docs/start/ 
    -  kubernetes :  https://kubernetes.io/docs/setup/ 
    -  docker  :  https://www.docker.com/get-started 
    -  pulumi  :  https://www.pulumi.com/docs/install/

Steps:
    - Build the dockerfile locally: 
        (cmd):
            'docker build -t <image_name> .'
            'docker tag <new image name> <dockerHub userName>/<new image name>:latest'
            'docker push <dockerHub userName>/<new image name>:latest'

    - Initialize & deploy a New Pulumi Project: 
        create new dir : "pulumi"
        create python envirenment (.venv)
        (cmd):
            Activate your virtual environment : '.venv\Scripts\activate' or 'source .venv/bin/activate' 
            'cd /pulumi'
            'pulumi new kubernetes-python'
            'pulumi up'

    - Make sure its works: 
        (cmd):
            'kubectl get services'
            'minikube service <service_name>' --> return url 
        