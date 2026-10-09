# Web server (Enhanced + NodePort Service)
Simple web server that prints `Server started with RANDOM_STRING`.
And returns 2 random strings (one is fixed to each running instance of the server) on / endpoint for GET requests.

`kubectl apply -f ./manifests/deployment.yaml`
or you can deploy it without cloning the repo 
`kubectl apply -f https://raw.githubusercontent.com/AhmadNajiKam/KubernetesSubmissions/refs/tags/1.6/web_server/manifests/deployment.yaml`

To test it in development apply the NodePort service: 
`kubectl apply -f ./manifests/service.yaml`

You can also change the value of the PORT variable in the manifest file, but make sure to change the targetPort in service.yaml.
