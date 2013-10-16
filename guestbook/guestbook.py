from google.appengine.ext import ndb
import webapp2


class Guest(ndb.Model):
    name = ndb.StringProperty(required=True)
    register_date = ndb.DateTimeProperty(auto_now_add=True)


class GuestBook(ndb.Model):
    name = ndb.StringProperty(required=True)
    guests = ndb.KeyProperty(repeated=True)

    def list_guests(self):
        return [guest.get() for guest in self.guests]

    @classmethod
    def find_or_create(cls, name):
        guestbook = GuestBook.query(GuestBook.name == name).get()
        if not guestbook:
            guestbook = GuestBook(name=name, guests=[])
        return guestbook


MAIN_PAGE_HTML = """\
<html>
  <body>
    <h3>Sign a user on a guestbook:</h3>
    <form action="/sign" method="post">
      <div>Guestbook</div>
      <div><input type="text" name="guestbook" rows="3" cols="60"></input></div>
      <div>User Name</div>
      <div><input type="text" name="name" rows="3" cols="60"></input></div>
      <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <div><a href="/guestbooks">View Guestbooks</a></div>
  </body>
</html>
"""


class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_HTML)


class Sign(webapp2.RequestHandler):

    def post(self):
        guestbook = GuestBook.find_or_create(self.request.get('guestbook'))
        guest = Guest(name=self.request.get('name'))
        guest.put()
        guestbook.guests.append(guest.key)
        guestbook.put()
        self.redirect('/')


class Guestbooks(webapp2.RequestHandler):

    def get(self):
        guestbooks = GuestBook.query().fetch()
        for guestbook in guestbooks:
            self.response.write("<h3>" + guestbook.name + "</h3>")
            for guest in guestbook.list_guests():
                self.response.write("<p>" + guest.name + "</p>")
            self.response.write("<br>")
        self.response.write("<p><a href='/'>Voltar</a></p>")

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Sign),
    ('/guestbooks', Guestbooks),
], debug=True)