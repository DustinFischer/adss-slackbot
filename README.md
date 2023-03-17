# ADSS Slack Bot PoC

## Slack App
1. Create Slack app in Slack Api (TODO add link) by copying `mainfest.yaml`
2. Install `ngrok`
3. Set up a public proxy to your localhost
    ```
    $ ngrok http 5000
    ```
4. Get the public https endpoint
5. Set the Oauth redirect url in slack app Oauth and Permissions config (Note: oauth redirect url host is ngrok url)
6. Add a `.env` file, should look something like this:
    ```
    BASE_URL=https://xxx-xxx-xxx.eu.ngrok.io
    
    SLACK_CLIENT_ID=hij.789
    SLACK_CLIENT_SECRET=def456
    SLACK_SIGNING_SECRET=abc123
    
    ADSS_API_TOKEN=eyour.jwt.token
    ```
7. Run the app
    ```
    $ flask --app main run
    ```
## User Notifications

For reference: [Slack Camel example github](https://github.com/apache/camel-kafka-connector-examples/tree/main/slack/slack-sink)
1. Find the webhook url for your app installation and update in `notifications/config/KafkaSlackCamelSinkConnector.conf`
2. Note, the channel config does not appear to be working at time of writing, so messages will only be routed to the webhook url installed channel
3. [Download Kafka Camel Slack Sink Connector tar](https://camel.apache.org/camel-kafka-connector/3.18.x/reference/index.html)
4. Unpack (tar etc.) and move to local plugins folder `/tmp/custom/jars`
5. Have Kafka installed locally (optional, just for the CLI commands)
6. Run Kafka connect
   ```
   $ docker compose up connect
   ```
7. Wait for connect to be active (poll it and wait for a response):
    ```
    $ curl localhost:8083
    ```
8. Create a `slack-notifications` topic on kafka
   ```
   $ kafka-topics --bootstrap-server localhost:9092 --topic slack-notifications --create
   ```
9. Start the Slack Camel connector 
    ```
    $ curl -XPOST -d @notifications/config/KafkaSlackCamelSinkConnector.conf -H "Content-Type: application/json" http://localhost:8083/connectors | jq '.'
    ``` 
10. Produce a message to the `slack-notifications` topic
     ```
     $  kafka-console-producer --bootstrap-server localhost:9092 --topic slack-notifications
    
     > Hello!!!
     >
     ```
11. The message should appear in `#adss-notifications` Slack channel