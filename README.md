# Process Receipts

This is my implementation of fetch's [receipt-processor-challenge](https://github.com/fetch-rewards/receipt-processor-challenge). It uses python and the [FastAPI](https://fastapi.tiangolo.com/) framework.

## Building and Running

This application has a Dockerfile. At the root directory of this project, you can use the following command to build the image:

`docker build -t receipt-processor-challenge .`

And the command to run it:

`docker run -d --name receipt-container -p 8000:8000 receipt-processor-challenge`

## Accessing and using the API

Once the Docker container is running there are multiple ways to use the API.

1. Navigate to `http://127.0.0.1:8000/docs` or ` to view the Swagger documentation.
   This is interactive API documentation with examples and allows a user to type in their request.

2. CLI via curl:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/receipts/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "retailer": "M&M Corner Market",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    }
  ],
  "total": "6.49"
}'
```

```
curl -X 'GET' \
  'http://127.0.0.1:8000/receipts/{id}/points' \
  -H 'accept: application/json'
```
