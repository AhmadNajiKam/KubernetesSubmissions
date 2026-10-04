# Web server
Simple web server that prints `Server started in port NNNN`.

### 1. Build and push

```bash
docker build -t YOUR_USERNAME/image_name .
docker push YOUR_USERNAME/image_name
```
```
kubectl create deployment <deployment_name> --image=YOUR_USERNAME/image_name --port=3000
kubectl set env deployment/<deployment_name> PORT=<port>
```
```
```
```
