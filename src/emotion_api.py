# Basic emotion API
# Can analyse a picture given its url and print how 'scared'
# each face is from left to right

import json
import numpy as np
import cv2
import http.client, urllib.request, urllib.parse, urllib.error, base64, sys

# Global parameters, use your own key for subscription
MY_SUBSCRIPTION_KEY = insert your own key here

HEADERS_URL = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': MY_SUBSCRIPTION_KEY
}
HEADERS_FILE = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': MY_SUBSCRIPTION_KEY
}

URL_GLOBAL_PARAMS = urllib.parse.urlencode({
})

HTTPS_CONNECTION = 'westus.api.cognitive.microsoft.com'

# This takes a filepath to a picture (.jpg/.png/whatever) and then converts that
# filepath to a different extension keeping the entire file structure the same
# `ext` is the extension we are going to add instead
def get_out_filename(filepath, ext):
    posn = filepath.rfind('.')
    new_path = filepath[:posn]
    return (new_path + ext)

# gets area of a face
def get_face_area(face):
    return (face['faceRectangle']['width'] *\
            face['faceRectangle']['height'])

# Takes a url to an image and returns the scores for all faces in the image,
# from the biggest face to the smallest face
# @param filepath is a string- either an absolute URL or an
#                 absolute filepath
# @param is_url is True if you are analysing an image from the net, and False if
#               you are analysing a local file
def analyse_picture(filepath, is_url):

    if is_url:
        # Replace the example URL below with the URL of the image you want to analyze.
        body = "{ 'url': '" + filepath + "' }"
        HEADERS = HEADERS_URL
    else:
        fin = open(filepath, 'rb')
        body = fin.read()
        fin.close()
        HEADERS = HEADERS_FILE

    try:
        # NOTE: You must use the same region in your REST call as you used to
        # obtain your subscription keys.  For example, if you obtained your
        # subscription keys from westcentralus, replace "westus" in the URL
        # below with "westcentralus".
        conn = http.client.HTTPSConnection(HTTPS_CONNECTION)
        conn.request("POST", "/emotion/v1.0/recognize?%s" % URL_GLOBAL_PARAMS,
                body, HEADERS)
        response = conn.getresponse()
        data = response.read()
        # 'data' contains the JSON data. The following formats the JSON data for
        # display.
        parsed = json.loads(data.decode())

        if 'error' in parsed:
            print("Data has an error")
            raise Exception(parsed['error'])
        elif 'statusCode' in parsed:
            print("Data has a status code")
            raise Exception(parsed['message'])
        else:
            parsed = sorted(parsed, key = lambda k: get_face_area(k), reverse = True)
            conn.close()
            return parsed

    except Exception as e:
        print("Caught exeption")
        print(data)
        print(parsed)
        print(e.args)

# A basic function that converts a face dictionary into a raw 'scared' value
# which it returns, and also returns a dictionary of the match for all the other
# emotions
def how_scared(face):
    scores = face['scores']

    # the weights we assign to each other emotion
    W_ANGER      = 0.0
    W_CONTEMPT   = 0.0
    W_DISGUST    = 0.0
    W_FEAR       = 0.8
    W_HAPPINESS  = 0.0
    W_NEUTRAL    = 0.0
    W_SADNESS    = 0.0
    W_SURPRISE   = 0.2
    # some base value that we use to shift the scale
    BASE         = 0.0

    # how scared we think the face in the picture is
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

# writes the 'fear of a face' to a file
def output_scared(face, filepath):

    with open(filepath, 'w') as fout:
        val = how_scared(face)
        fout.write('scared: ')
        fout.write(str(val) + '\n')

        scores = face['scores']
        for emotion in scores:
            fout.write(emotion + ': ')
            fout.write(str(scores[emotion]) + '\n')

if __name__ == "__main__":
    #initialise camera 
    cap = cv2.VideoCapture(0)

    #capture
    _,image = cap.read()
    print('photo taken')
    
    # Display the resulting frame
    cv2.imwrite('picworks.png', image)

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    #analyse data
    data = analyse_picture('picworks.png', is_url = False)   

    output_scared(data[0], "picworks.out")
