<h1> Django-AB-project </h1>
<p>Here is my first package for <b>Django</b>. I tried to write it so that it would be easy for you to use this package.</p>

<p>It provide four function in utils.py and some models in models.py.</p>
<p>This would be easy to used this package with Generic views in Django, but this can be work properly in methods, just used another technic.</p>

(You can read about Generic Views in Django here - https://docs.djangoproject.com/en/1.11/topics/class-based-views/)
<h2>What is A/B testing?</h2>
A/B testing (also known as split testing) is a method of comparing two versions
of a webpage against each other to determine which is better for users.
AB testing is essentially an experiment where two variations of a page are shown to users in random order (In this package all users are divided
to two group, and not needed to registrated in your app)
and statistical analysis is used to determine which variation performs better for a given conversion goal.
<br><br>
<h2>How to install?</h2>
  1. Use pip to download this package - <b><i>pip install django-AB-project</i></b>
  <br><br>
  2. Add <i>'ab',</i> to <b>INSTALLED_APPS</b> in settings.py
  
```Python
  INSTALLED_APPS = [
    ...
    ...
    'ab',
  ]
```
  3. Configure your sessions - set in settings.py at the end of file (or where you want): 

```Python
  SESSION_EXPIRE_AT_BROWSER_CLOSE = True # Coockie's will be destroyed after browser close
  SESSION_COOKIE_AGE = 60 * 60 * 24 # Coockie's will be destroyed after 24 hours
```
  You can edit this lines if you need.
  <br><br>
  4. Run <b><i>python manage.py makemigrations</i></b>, and <b><i>python manage.py migrate</i></b>
  <br><br>
  5. Run server (<i>python manage.py runserver</i>) and go to the admin page. If you see new line named <i>"Ab_Split_Testing"</i> and can click on them without error page - Congratulation! You successfully installed this package.
  
<h2>How to use?</h2>
<i>This package have two main function for each version of views</i>
<br>
<i>(Generic views version)</i>
<br><br>
<p>Let's imagine we have some ListView in <b><i>views.py</i></b></p>

```Python
  from django.views.generic import ListView

  class IntroPage(ListView):
    model = YourModel
    template_name = 'pages/intro.html'
```

<p>First function, called <b>ab_init</b> we need to use when page is loading, to check if user is load this page.</p>
<p>But also, we need some varables (like path to alternative html file, and name for test)</p>
<p>Let's define!</p>



```Python
  class IntroPage(ListView):
    model = YourModel
    template_name = 'pages/intro.html'
    alternative_template_name = 'alt_pages/intro.html'
    page_name = 'intro page'

    def dispatch(self, request, *args, **kwargs):
        # init for a/b, add +1 to "Entered"
        ab_init(self)
        # call the view
        return super(IntroPage, self).dispatch(request, *args, **kwargs)
```
<p>Let see what we got:</p>

```Python
   alternative_template_name = 'alt_pages/intro.html'
```
<p>Here you need to enter a path to your alternative html file, which you want to test with <i><b>template_file</b></i></p>
<p>Next is:</p>

```Python
   page_name = 'intro page'
```
<p>Enter a name for this page(this test will be named like that)</p>
<p>Next scary thing:</p>

```Python
    def dispatch(self, request, *args, **kwargs):
        # init for a/b, add +1 to "Entered"
        ab_init(self)
        # call the view
        return super(IntroPage, self).dispatch(request, *args, **kwargs)
```
<p>This function will be called when page is loading, so it's perfect place where a/b will be initialized</p>
<p>Let's test our page, go to the urls.py, and write this code: </p>

```Python
    from django.conf.urls import url
    from . import views

    urlpatterns = [
         url(r'^$', views.IntroPage.as_view(), name='intro_page'),
    ]
```
<p>Run your server, and go to <b><i>127.0.0.1:8000/</i></b></p>
<p>If you don't see any error, and page looks like normal - go to the admin page and check <i>"Ab_Split_Testing"</i>!</p>
<p>Here you see new created object, using your <i>page_name</i>. Click on and you will see some data. Run another browser, or
re-enter in your browser and load main page again, and you will see changes.</p>
