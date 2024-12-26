# Socket-IO with Runpod Serverless
This document explains how to run the socket-io server on Runpod serverless. Here are the steps for this purpose
1. A template is provided that will activate the socket-io on serverless when request will start.
2. Modify it as you want and then deploy this template to your Runpod in serverless.
   1. Expose HTTP port `3000` for socket-io in Docker configurations.
   2. Uncheck `Enable Execution Timeout` to disable auto pod request timeout that will terminate the serverless job or set a value if you want to set the max time for running a socket-io server. 
3. Initiate a request with following command
    ```shell
    curl --location 'https://api.runpod.ai/v2/{{endpoint_id}}/run' \
   --header 'Content-Type: application/json' \
   --header 'Authorization: Bearer {{API_KEY}}' \
   --data '{"input": {"key": "value"}}'
    ```
4. It will start socket-io server on your serverless pod and your pod will stay active until you turn it off manually with the request give below.
5. As Runpod serverless can have many workers and different request will go to different workers. The socket-io address will be different on each worker. To get the socket-io address from the worker where you initiated, call the following API 
    ```shell
    curl --location --request POST 'https://api.runpod.ai/v2/{{endpoint_id}}/status/{{job_id}}' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer {{API_KEY}}'
    ```
   Where you will get `job_id` from the previous API request response.
6. If the server has started, then it will return the `status=IN_PROGRESS` in the response of above API. In this case, it will also return the `workerId`. 
7. Now, you can connect to socket-io by using following address
    ```shell
    wss://{{workerId}}-3000.proxy.runpod.net
    ```
   Where 3000 is your exposed port. 
8. To test if your socket server is running, a test page also has provided here which you can access by running following url in your browser:
   ```shell
   https://{{workerId}}-3000.proxy.runpod.net
   ```
   Or manually go to your worker in Runpod console, select the running worker, then click on the `connect` button and after few seconds it will show the button to go to exposed port 3000 in the open popup window. By clicking on that button, you will be redirected to a new window in the browser where you can test the socket io connection.
9. Remember to turn off the serverless server when you have completed your job with socket-io by using the following API
    ```shell
    curl --location --request POST 'https://api.runpod.ai/v2/{{endpoint_id}}/cancel/{{job_id}}' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer {{API_KEY}}'
    ```