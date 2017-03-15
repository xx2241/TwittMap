# TwittMap
## COMSW6998 Clouding Computing and Big Data
## Assignment 1: TwittMap with Trends
<br>
HW Group 30 <br>
Authors: <br>
**Kuang Yang**, **ky2342** <br>
**Xun Xue**, **xx2241**

### Step 1: Create Amazon Elasticsearch Service domain
* We choose **Elasticsearch** version 2.3. The instance type is t2.micro. The storage type is EBS.
* Select the access policy to allow open access to the domain for simplicity. You should choose a stricter policy in the real-world application.

### Step 2: Create Index on AWS Elasticsearch
* Run the command below in the terminal(This command is stored in the file *create_initial_index*). In the endpoint of domain *twittmap*, it creates an index(database) called *twittmap* with its type as *tweets*.
```
curl -XPUT search-twittmap-lvm7h7c3kpkrzia336fisfesku.us-east-1.es.amazonaws.com/twittmap -d '
{
    "mappings": {
        "tweet": {
            "properties": {
                "keyword": {
                    "type": "string"
                },
                "author": {
                    "type": "string",
                    "index": "not_analyzed"
                },
                "text": {
                    "type": "string"
                },
                "timestamp": {
                    "type": "date"
                },
                "coordinates": {
                    "type": "geo_point"
                }
            }
        }
    }
}'
```

### Step 3: Collect Tweets Streaming
* Run `pip install -r requirements.txt` first to install dependencies.
* Run `python twitter_streaming.py`.
* This program uses **Twitter Streaming API** and **Tweepy** to fetch tweets from the twitter hose in real-time.
* This program stores processed and structured data on **AWS Elasticsearch**.
* Link to Tweepy: https://github.com/tweepy/tweepy
* Comments: This application can run under both Python2 and Python3 environment. **However, Python2 is more preferred**. If you encountered any issues, make sure you test under Python2 environment. If you have any problems in collecting tweets streaming, update your Tweepy first and restart this script manually. Thanks!

### Step 4: Create Web UI
* Create a Web UI using **HTML** and **JavaScript** to allow users to choose any keyword(up to 10) through a dropdown box.
* Initialize **Google Map** using **Google Maps API**.

### Step 5: Filter Tweets
* Use **Python** **Flask** framework as the backend server connected to **AWS Elasticsearch**.
* Use **AJAX** and **jQuery** to communicate between the frontend and backend.
* Query tweets data on Elasticsearch according to the keyword selected by the user in the frontend.
* Bonus: Filter tweets using ElasticSearch’s geospatial feature that shows tweets that are within a certain distance from the point the user clicks on the map.

### Step 6: Visualize Filtered Tweets
* For keyword filter, I use Heatmap to visualize the density of tweets distributions.
* For gepspatial feature filter, I add a listener event to each marker. Whenever the user clicks the marker, an infowindow is popped out to show the contents of the tweet and its author. For the point which the user clicks on, I attach a red marker on it every time, and when you click on it, it will pop out an infowindow to show its coordinates.

### Step 7: Deploy the Web App on AWS Elastic Beanstalk
* To deploy **Python Flask** web app on **AWS Elastic Beanstalk**, see documents here: http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
* Here I use **Python2.7** environment. Also, when you zip your project, please remember that first `cd` into the root directory of your project and then zip all codes and file. Don't zip them in the same level of your project folder.

### Link to My TwittMap Web App:
* http://twittmap-group30.xbsfi2zcmp.us-east-1.elasticbeanstalk.com/
