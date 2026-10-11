To deploy this service make sure you do the following (Don't do again for todo-app):


`k3d cluster create test -p "8082:30080@agent:0" -p "8081:80@loadbalancer" --agents 2 `

`docker exec k3d-test-agent-0 mkdir -p /tmp/image`

`kubectl apply -f ./manifests`
