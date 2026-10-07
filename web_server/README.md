# Web server (Enhanced)
Simple web server that prints `Server started with RANDOM_STRING`.
And returns 2 random strings (one is fixed to each running instance of the server) on / endpoint for GET requests.

`kubectl apply -f ./manifests/deployment.yaml`
or you can deploy it without cloning the repo 
`kubectl apply -f https://raw.githubusercontent.com/AhmadNajiKam/KubernetesSubmissions/refs/tags/1.5/web_server/manifests/deployment.yaml`

To test it in development do port forwarding: 
`kubectl port-forward pod <pod_name> <local_port>:<remote_port>
`

You can also change the value of the PORT variable in the manifest file, but make sure to change the remote_port accordingly.
