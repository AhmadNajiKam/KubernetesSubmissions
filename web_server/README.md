# Web server (Enhanced + ClusterIP Service + Ingress)
Simple web server that prints `Server started with RANDOM_STRING`.
And returns 2 random strings (one is fixed to each running instance of the server) on / endpoint for GET requests.

To deploy all parts together:
`kubectl apply -f ./manifests`
