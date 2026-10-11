To deploy do the following:

`k3d cluster create test -p "8082:30080@agent:0" -p "8081:80@loadbalancer" --agents 2 `

`docker exec k3d-test-agent-0 mkdir -p /tmp/kube`


`kubectl apply -f ./`
`kubectl apply -f ../log_output/manifests`
`kubectl apply -f ../ping-pong-application/manifests`

You can test the app by first visiting localhost:8081/pingpong to generate a counter, after that you can reference localhost:8081/ to check logoutput response.
