## log_output project

To deploy it on Kubernetes use the following command:
`kubectl create deployment <deployment_name> --image=hexa4d/log_output`

Which will pull the image from DockerHub, or you can write the following if you wanna build the image one your device:
````
```
clone https://github.com/AhmadNajiKam/KubernetesSubmissions.git
cd log_output/
docker build -t <image_name> .
k3d image import <image_name> -c <cluster_name>
kubectl create deployment <deployment_name> --image=<image_name>
kubectl patch deployment <deployment_name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<deployment_name>","imagePullPolicy":"Never"}]}}}}'
```

