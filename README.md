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
  <br>
  2. Add 'ab', to INSTALLED_APPS in settings.py:

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
  from split_testing.utils import ab_init, success_goal

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
<p>Here you need to enter a path to your alternative html file, which you want to test with <i><b>template_name</b></i></p>
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
<p>We successfully initialized our test, but we need collect not only users who entered to our page, but also users, who will make success actions. It would be simple if you need to test forms on your page, but we can test other element's too, just use a little bit of JavaScript.</p>

<h3>Testing with forms</h3>
<p>ab_init method say if user successfully loaded page, and also remember which page need to show in next time, but to make A/B testing come to life, we need some more extra functionality, like when user do successful action.
</p>
<p><b>Hey, but what is "successful action"?</b> you might want to ask. Let's imagine shop page, and big "BUY" button. You need define, which button will give more sales, red or green. You created two pages, which looks like the same, but with different buttons, and then, when users will find your page, system will remember all users, and which percent of them clicked by this button. After a few days\weeks, when you collect enough of information, you will see in percentage, which button makes more revenue.</p>


<p>A useful thing, right? So here we have two ways to do that, first, when we have form on our page:</p>


```Python
from django.shortcuts import redirect
from django.views.generic import FormView
from split_testing.utils import ab_init, success_goal

class SecondPage(FormView):
    # A/B testing variables
    template_name = 'pages/second_page.html'
    alternative_template_name = 'alt_pages/second_page.html'
    page_name = 'second page'
    form_class = someForm
    
    def dispatch(self, request, *args, **kwargs):
        # init for a/b, add +1 to "Entered"
        ab_init(self)
        # call the view
        return super(SecondPage, self).dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        # Process your forms
        ... 
        ...
        # A/B set successfully goal before redirect
        success_goal(self)
        
        return redirect('third_page')
```
<p><i>success_goal(self)</i> is <b>second</b> function what this package implement.</p>
<p>When this function is triggered, system will remember this action, and to prevent when user click by this button a lot, and to not screw up our experiment, will be saved just one click per user.</p>


<h3>Testing using JS (jQuery, actually)</h3>
<p>First, you need edit your both html files. Just add to bottom of the body tag this function:</p>
  
```javascript
  <script type="text/javascript">
    function Sendgoal(url_page) {
      $.ajax({
        url: url_page,
        data: {'is_clicked': 'True',
                csrfmiddlewaretoken: "{{ csrf_token }}"},
        type:"POST",
        success: function (data) {
          console.log('POST success');
        },
      });
    }
  </script>
```
<p>Then, you need find your button, or link which pressed by user will be send goal to server</p>

```html
<a href='#' onclick="Sendgoal('{% url 'intro_page' %}')">Click me!</a>
```
<p>Our work in HTML files is done, now we need to edit our IntroPage class, to handle POST requests:</p>

```python
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
        
    def post(self, request, *args, **kwargs):
        is_clicked = request.POST.get('is_clicked')
        if is_clicked == 'True':
            # A/B set success goal
            success_goal(self)
            return JsonResponse({'OK':'OK'})
        # if POST request is not equal what we send in template
        return JsonResponse({'KO':'KO'})
```

  <p>That's it! Your test is ready, try to test it using another browser.</p>
  
  <p>But if you don't know how method post work, lets read it step-by-step:</p>
  
  <p>Here we are define our method, and get from POST request if user actually click our element</p>
  ```python
    def post(self, request, *args, **kwargs):
        is_clicked = request.POST.get('is_clicked')
  ```
  
  <p>If <b>is_clicked</b> equal to <b>'True'</b> string, we will call success_goal method, and save it to the system.</p>
  ```python
    if is_clicked == 'True':
            # A/B set success goal
            success_goal(self)
  ```
  
  and then we just return some data into our html, to clarify, if method register or not our goal.
  
  
<br>
<i>(Method views version)</i>
<br><br>
<p>Coming soon!</p>
