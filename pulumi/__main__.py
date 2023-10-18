import pulumi
from pulumi_kubernetes.apps.v1 import Deployment, DeploymentSpecArgs
from pulumi_kubernetes.meta.v1 import LabelSelectorArgs, ObjectMetaArgs
from pulumi_kubernetes.core.v1 import ContainerArgs, PodSpecArgs, PodTemplateSpecArgs, ResourceRequirementsArgs, VolumeArgs, VolumeMountArgs
from pulumi_kubernetes.core.v1 import PersistentVolumeClaimVolumeSourceArgs, PersistentVolumeClaim
from pulumi_kubernetes.core.v1 import Service, ServiceSpecArgs, ServicePortArgs

# Define labels for the Nginx pods
app_labels = {"app": "nginx"}

# Create a Persistent Volume Claim (PVC)
nginx_pvc = PersistentVolumeClaim(
    "nginx-pvc",
    metadata={"name": "nginx-pvc"},
    spec={
        "access_modes": ["ReadWriteOnce"],
        "resources": {"requests": {"storage": "1Gi"}},
        "storage_class_name": "standard"  # Specify the storage class
    }
)

# Create a Kubernetes Deployment for Nginx
nginx_deployment = Deployment(
    "nginx-deployment",
    spec=DeploymentSpecArgs(
        replicas=4,  # Create 4 Nginx pods
        selector=LabelSelectorArgs(match_labels=app_labels),
        template=PodTemplateSpecArgs(
            metadata=ObjectMetaArgs(labels=app_labels),
            spec=PodSpecArgs(
                containers=[
                    ContainerArgs(
                        name="nginx",
                        image="yosefha4/new-img-nginx:latest",  # Use the Nginx official image
                        image_pull_policy="IfNotPresent",  # Set the image pull policy to "IfNotPresent"
                        resources=ResourceRequirementsArgs(
                            requests={"cpu": "100m", "memory": "128Mi"},  # Resource requests
                            limits={"cpu": "200m", "memory": "256Mi"}  # Resource limits
                        ),
                        volume_mounts=[
                            VolumeMountArgs(
                                name="nginx-persistent-storage",
                                mount_path="/usr/share/nginx/html"
                            )
                        ],
                    )
                ],
                volumes=[
                    VolumeArgs(
                        name="nginx-persistent-storage",
                        persistent_volume_claim=PersistentVolumeClaimVolumeSourceArgs(
                            claim_name=nginx_pvc.metadata["name"]
                        )
                    )
                ],
            )
        ),
    ),
)

# Create a Kubernetes Service to expose Nginx ports
nginx_service = Service(
    "nginx-service",
    spec=ServiceSpecArgs(
        selector=app_labels,  # Select the Nginx pods by labels
        ports=[
            ServicePortArgs(name="http", port=80, target_port=80),  # HTTP
            ServicePortArgs(name="https", port=443, target_port=443),  # HTTPS
        ],
        type="NodePort",  # Expose the service using NodePort
    ),
)

# Export the Deployment name for reference
pulumi.export("nginx-deployment-name", nginx_deployment.metadata["name"])
pulumi.export("nginx-service-url", nginx_service.spec.ports[0].node_port)  # Use this URL to access the service
