# Todo App

First create the cluster and the directory inside the node you need to persist data to it:
`k3d cluster create test -p "8082:30080@agent:0" -p "8081:80@loadbalancer" --agents 2 `
`docker exec k3d-test-agent-0 mkdir -p /tmp/image`
To deploy all parts together:
`kubectl apply -f ./manifests`

You can access it via localhost:8081/

Note: Don't create the cluster again if you did that in todo-backend setup
