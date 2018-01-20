# Basic emotion API
# Can analyse a picture given its url and print how 'scared'
# each face is from left to right

import json
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

# Global parameters, use your own key for subscription
HEADERS = {
    # Request headers. Replace the placeholder key below with your subscription key.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '<demo>',
}

URL_GLOBAL_PARAMS = urllib.parse.urlencode({
})

HTTPS_CONNECTION = 'westus.api.cognitive.microsoft.com'

# takes a url to an image and returns the scores for all faces
# in the image, from left to right
def analyse_picture(url):
    # Replace the example URL below with the URL of the image you want to analyze.
    body = "{ 'url': '" + url + "' }"

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection(HTTPS_CONNECTION)
        conn.request("POST", "/emotion/v1.0/recognize?%s" % URL_GLOBAL_PARAMS,
                body, HEADERS)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        parsed = sorted(parsed, key = lambda k: k['faceRectangle']['left'])
        conn.close()
    except Exception as e:
        print(e.args)

    return parsed

# a basic function that converts the list of scores into a raw
# 'scared' value
def how_scared(face):
    scores = face['scores']

    W_ANGER      = 0.0
    W_CONTEMPT   = 0.0
    W_DISGUST    = 0.0
    W_FEAR       = 0.8
    W_HAPPINESS  = 0.0
    W_NEUTRAL    = 0.0
    W_SADNESS    = 0.0
    W_SURPRISE   = 0.2
    BASE         = 0.0

    val = scores['anger']    * W_ANGER      +\
          scores['contempt'] * W_CONTEMPT   +\
          scores['disgust']  * W_DISGUST    +\
          scores['fear']     * W_FEAR       +\
          scores['happiness']* W_HAPPINESS  +\
          scores['neutral']  * W_NEUTRAL    +\
          scores['sadness']  * W_SADNESS    +\
          scores['surprise'] * W_SURPRISE   +\
          BASE

    return(val)

data = analyse_picture('<demo>')

for obj in data:
    print (how_scared(obj))
