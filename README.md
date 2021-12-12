# Flask Key Server App Deployment on K8s

This project is about hosting a Dockerized Flask app on k8s using helm.
The Flask app stores key-value in memory with features of fetching and searching them. Check out list of APIs below for features.

- [Flask Key Server App Deployment on K8s](#flask-key-server-app-deployment-on-k8s)
  - [Build Docker Image](#build-docker-image)
  - [Push Docker Image](#push-docker-image)
  - [Run Test Cases](#run-test-cases)
    - [Examples](#examples)
      - [Run only unit tests](#run-only-unit-tests)
      - [Run only integration tests](#run-only-integration-tests)
  - [Deploy App](#deploy-app)
    - [Debug helm templates](#debug-helm-templates)
    - [uninstall helm](#uninstall-helm)
  - [Setup Ingress](#setup-ingress)
  - [Setup CertManger](#setup-certmanger)
  - [Open/Use App](#openuse-app)
  - [Endpoints](#endpoints)
    - [Get Specific Key](#get-specific-key)
      - [Endpoint](#endpoint)
      - [Parameters](#parameters)
      - [Request](#request)
      - [Response](#response)
    - [Get All Keys](#get-all-keys)
      - [Endpoint](#endpoint-1)
      - [Parameters](#parameters-1)
      - [Request](#request-1)
      - [Response](#response-1)
    - [Set Key](#set-key)
      - [Endpoint](#endpoint-2)
      - [Parameters](#parameters-2)
      - [Request](#request-2)
      - [Response](#response-2)
    - [Search Keys](#search-keys)
      - [Endpoint](#endpoint-3)
      - [Parameters](#parameters-3)
      - [Request](#request-3)
      - [Response](#response-3)
    - [Monitoring](#monitoring)
      - [Endpoint](#endpoint-4)
      - [Parameters](#parameters-4)
      - [Request](#request-4)

## Build Docker Image

```bash
docker build -t dsdatsme/key-server-flask:<tag> .
```

## Push Docker Image

Make sure you have logged in to your docker hub account(or any other registry) on your local.

```bash
docker push dsdatsme/key-server-flask:<tag>
```

## Run Test Cases

Project uses `unittest` python library to write our test cases. The test cases are inside folder [test](./key_server_app/test).

There are two folders to separate [unit test](./key_server_app/test/unit_tests) and [integration tests](./key_server_app/test/integration_tests) .

If you wish to run the test case you can refer the following command.

```bash
docker run -t dsdatsme/key-server-flask:<Image Tag> pytest <options>
```

### Examples

Following are some ways to run test cases

#### Run only unit tests

```bash
docker run -t dsdatsme/key-server-flask:v2 pytest -m unittest --cache-clear --verbose --disable-warnings
```

#### Run only integration tests

```bash
docker run -t dsdatsme/key-server-flask:latest pytest -m integrationtest --cache-clear --verbose --disable-warnings
```

## Deploy App

Once desired docker image is built and pushed to registry, we can then deploy the app. In this project we are using helm chart to manage and deploy various app resources.

```bash
helm create key-server-app-chart

helm upgrade --install key-server-chart key_server_helm --values key_server_helm//values.yaml --namespace key-server-app --create-namespace --debug
```

### Debug helm templates

```bash
helm template key_server_helm --debug
```

### uninstall helm

```bash
helm uninstall  --namespace coresystem publicingress
```

## Setup Ingress

```bash
# creating a namespace for ingress-nginx
kubectl create namespace coresystem
# setting up ingress
 helm upgrade --install --namespace coresystem publicingress ingress-nginx/ingress-nginx -f ingress-nginx/ingress-values.yaml --debug
 # get loadbalancer IP, there you will see nginx controller of type LB
kubectl get svc --namespace coresystem
```

## Setup CertManger

To setup CM, please refer the project files  [DSdatsme/golang-api-k8s-ci-cd](https://github.com/DSdatsme/golang-api-k8s-ci-cd#cert-manager).

The setup is simple, and should not take much effort to deploy.

## Open/Use App

Once app is deploy, you can access the app using the domain.
To setup domain locally:

- Get the ip/dns of your ingressclass service.
- create an entry in `/etc/hosts` file with the domain in `values.yaml` file. Eg:
  > 10.109.3.126 dsdatsme.ddns.net
- Now you have you make sure your local is able to access that IP. If you are using minikube you can use tunnel feature by running the command 

  ```bash
  minikube tunnel
  ```

- Open browser and hit the domain with `/get` endpoint like shown in the image.
![GET call](/docs/get_all_keys.png)


## Endpoints

### Get Specific Key

<details>

<summary>Make a GET request with a key ID to get it's value</summary>

#### Endpoint

> GET /get/\<KEY ID>

#### Parameters

`KEY ID`: Pass the name of the key to URL endpoint.

#### Request

```bash
curl --location --request GET '<DOMAIN>/get/<KEY ID>'
```

Example:

```bash
curl --location --request GET 'https://dsadatsme.ddns.net/get/testkey'
```

#### Response

```json
{
  "body": {
      "value": "secretvalue"
  },
  "status_code": 200,
  "success": true
}
```

</details>

### Get All Keys

<details>

<summary>Make a GET request to get all keys</summary>

#### Endpoint

> GET /get

#### Parameters

No params required.

#### Request

```bash
curl --location --request GET '<DOMAIN>/get'
```

Example:

```bash
curl --location --request GET 'https://dsadatsme.ddns.net/get'
```

#### Response

```json
{
  "body": {
      "keys": {
          "key1": "idk",
          "key2": "passwd"
      }
  },
  "status_code": 200,
  "success": true
}
```

</details>

### Set Key

<details>

<summary>Make a POST request with desired data to store your key on server.</summary>

You can use this method to change the value of existing keys.

#### Endpoint

> POST /set

#### Parameters

`key_name`[REQUIRED]: Name/ID of the key.

`key_value`[REQUIRED]: Value of the key.

#### Request

```bash
curl --location --request POST 'https://<DOMAIN>/set' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "key_name": "<key_name>",
    "key_value": "<key_value>"
  }'
```

Example:

```bash
curl --location --request POST 'https://dsdatsme.ddns.net/set' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "key_name": "qwe",
      "key_value": "1234"
  }'
```

#### Response

```json
{
  "body": "Key created with ID qwe",
  "status_code": 201,
  "success": true
}  
```

</details>

### Search Keys

<details>

<summary>Make a GET request to fetch key IDs based on prefix and/or suffix search.</summary>

#### Endpoint

> GET /search?prefix=\<term>

> GET /search?suffix=\<term>
 
> GET /search?prefix=\<term1>&suffix=\<term2>

#### Parameters

> Atleast one parameter is required.

`prefix`: search based on prefix of the key name.

`suffix`: search based on suffix of the key name.

#### Request

```bash
curl --location --request GET 'https://<DOMAIN>/search?prefix=<prefixterm>'
```

Example:

```bash
curl --location --request GET 'https://dsdatsme.ddns.net/search?prefix=ke'
```

#### Response

```json
{
  "body": {
    "keys": ["key1", "key2"]
  },
  "status_code": 200,
  "success": true
}
```

</details>

### Monitoring

<details>

<summary>Make a GET request to fetch monitoring data.</summary>

This endpoint will be used by prometheus metrics scraper to get all the data from application.
#### Endpoint

> GET /metrics

#### Parameters

No parameters required.

#### Request

```bash
curl --location --request GET 'https://<DOMAIN>/metrics'
```
