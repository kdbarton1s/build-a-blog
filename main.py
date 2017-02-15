#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                                        autoescape = True)

class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("mainblog.html")
        content = t.render(blogs=blogs)
        self.response.write(content)


class BlogPage(webapp2.RequestHandler):
    def get(self):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5")
        t = jinja_env.get_template("mainblog.html")
        content = t.render(blogs=blogs)
        self.response.write(content)



class NewBlogPost(webapp2.RequestHandler):

    def get(self):
        t=jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        title = self.request.get("title")
        blog = self.request.get("blog")

        if title and blog:
            b = Blog(title = title, blog = blog)
            b.put()

            self.redirect("/blog/" + str(b.key().id()))

        else:
            error = "You must have both a title and content in the blog."
            t = jinja_env.get_template("newpost.html")
            content = t.render(title=title, blog=blog, error=error)
            self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        blog_id = Blog.get_by_id(int(id))
        if blog_id == None:
            error = "We couldn't find that post. Please try again."
            self.response.write(error)
        else:
            title = blog_id.title
            blog = blog_id.blog
            t = jinja_env.get_template("blogpost.html")
            content = t.render(title=title, blog=blog)
            self.response.write(content)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogPage),
    ('/newpost', NewBlogPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
