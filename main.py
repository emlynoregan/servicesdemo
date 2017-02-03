# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
from google.appengine.ext import deferred
import logging
import time

def HelloWorld():
    x = 0
    logging.info("Counting...")
    while x < 10000000:
        x += 1
    logging.info("Hello World")
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        # run HelloWorld in a background task on the background queue
        self.response.headers['Content-Type'] = 'text/html'
        self.response.write('''
<html>
<body>
  <form method="POST">
    <button type="submit" name="foreground" value="x">foreground</button>
    <button type="submit" name="background" value="x">background</button>
  </form>
</body>
'''
        )

    def post(self):
        def EnqueueTasks(aNumTasks, **kwargs):
            for _ in range(aNumTasks):
                deferred.defer(HelloWorld, **kwargs)         
            
        if self.request.get("foreground"):
            EnqueueTasks(10000)
            self.redirect("/")
        elif self.request.get("background"):
            EnqueueTasks(10000, _queue = "background")         
            self.redirect("/")
        else:
            self.response.write("wat")
        

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
