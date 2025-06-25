# 🛠️ Django-তে Base Template যোগ করা এবং ব্যবহার করার নিয়ম

## ✅ ধাপ ১: `base.html` তৈরি করা

**পাথ:**
`templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>{% block title %}EduLearn{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
    {% block extra_css %}{% endblock %}
  </head>
  <body>
    {% include 'partials/navbar.html' %}

    <main class="container">{% block content %}{% endblock %}</main>

    {% include 'partials/footer.html' %} {% block extra_js %}{% endblock %}
  </body>
</html>
```

---

## ✅ ধাপ ২: অন্য টেমপ্লেটে `base.html` এক্সটেন্ড করা

উদাহরণস্বরূপ `home.html` ফাইল:

**পাথ:**
`templates/home.html`

```html
{% extends 'base.html' %} {% block title %}Home - EduLearn{% endblock %} {%
block content %}
<h1>Welcome to EduLearn!</h1>
<p>This is your homepage.</p>
{% endblock %}
```

---

## ✅ ধাপ ৩: `settings.py` তে `TEMPLATES` কনফিগার চেক করা

```python
# settings.py

import os

TEMPLATES = [
    {
        ...
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```

---

## ✅ ধাপ ৪: স্ট্যাটিক ফাইলের জন্য কনফিগার

```python
# settings.py

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

---

## 🔁 টেমপ্লেট কোথায় রাখবো?

- `templates/base.html`
- `templates/app_name/home.html`
- `templates/partials/navbar.html` _(যদি ইনক্লুড করো)_

---

Django-তে যদি আপনি **একটি নির্দিষ্ট অ্যাপে static ফাইল (CSS, JS, images)** রাখতে চান, তাহলে আপনাকে কিছু নির্দিষ্ট নিয়ম মেনে চলতে হবে।
চলুন ধাপে ধাপে বাংলায় বুঝি — **“Django অ্যাপে static ফাইল ব্যবহারের সঠিক উপায়।”**

---

## ✅ ধাপ ১: অ্যাপের ভিতরে `static` ফোল্ডার তৈরি করুন

আপনার অ্যাপের ফোল্ডারে নিচের মত করে `static` ফোল্ডার বানান:

```
your_app/
├── static/
│   └── your_app/
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── script.js
│       └── images/
│           └── logo.png
├── templates/
│   └── ...
├── views.py
└── models.py
```

> 🔁 গুরুত্বপূর্ণ: `static/your_app/` এর মধ্যে রাখবেন, সরাসরি `static/css/` নয়।

---

## ✅ ধাপ ২: `settings.py`-এ `STATIC_URL` ও `STATICFILES_DIRS` নিশ্চিত করুন

### সাধারণভাবে এরকম থাকবে:

```python
# settings.py

STATIC_URL = '/static/'

# শুধু তখন দরকার যদি আপনি প্রজেক্ট লেভেলে static/ ফোল্ডার রাখতে চান
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # optional
```

**✅ অ্যাপ লেভেল `static`-এর জন্য আলাদা কিছু করতে হয় না। Django নিজেই খুঁজে পায়।**

---

## ✅ ধাপ ৩: টেমপ্লেট-এ স্ট্যাটিক ফাইল লোড করুন

### আপনার টেমপ্লেট ফাইলের শুরুতেই লিখুন:

```html
{% load static %}
```

### তারপর যেভাবে ফাইল ব্যবহার করবেন:

```html
<link rel="stylesheet" href="{% static 'your_app/css/style.css' %}" />
<script src="{% static 'your_app/js/script.js' %}"></script>
<img src="{% static 'your_app/images/logo.png' %}" alt="Logo" />
```

---

## ✅ ধাপ ৪: সার্ভার চালিয়ে দেখুন

```bash
python manage.py runserver
```

এরপর ব্রাউজারে চেক করুন ফাইলগুলো ঠিকভাবে লোড হচ্ছে কি না।

---

## 🔍 কেন `your_app/` prefix দিতে হয় static path-এ?

কারণ Django যখন অ্যাপ লেভেলের `static/` খুঁজে, তখন প্রত্যেক অ্যাপের static ফাইল আলাদা রাখতে `app_name` prefix ধরে।
এটা **name conflict** এড়াতে সাহায্য করে।

---

## 🎁 টিপস (Development vs Production):

- ডেভেলপমেন্টে: Django নিজেই static serve করে
- প্রোডাকশনে: আপনাকে `collectstatic` দিয়ে সব static ফাইল `STATIC_ROOT`-এ নিতে হয়

```bash
python manage.py collectstatic
```

---

## ✅ সংক্ষেপে:

| কাজ                 | কোথায়                                              |
| ------------------- | -------------------------------------------------- |
| অ্যাপের static ফাইল | `your_app/static/your_app/...`                     |
| টেমপ্লেটে ইউজ       | `{% static 'your_app/css/style.css' %}`            |
| settings.py         | `STATIC_URL` থাকা দরকার, `STATICFILES_DIRS` ঐচ্ছিক |
| লোড করতে            | `{% load static %}`                                |

---

Django-তে **media file** বলতে বোঝানো হয় user-uploaded ফাইল (যেমন ছবি, পিডিএফ, ডকুমেন্ট ইত্যাদি)।
এগুলো আপনার প্রজেক্টের static file থেকে আলাদা, এবং আলাদা ভাবে কনফিগার করতে হয়।

চলুন ধাপে ধাপে দেখি Django-তে media file কিভাবে যুক্ত করবেন ও ব্যবহারে আনবেন।

---

## ✅ ধাপ ১: `settings.py`-তে MEDIA কনফিগার যুক্ত করুন

```python
import os

# settings.py

MEDIA_URL = '/media/'  # URL path যেখানে ফাইল serve হবে
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # ফিজিক্যাল লোকেশন যেখানে ফাইল থাকবে
```

---

## ✅ ধাপ ২: `urls.py`-তে মিডিয়া সার্ভ করার জন্য কনফিগার (development-এর জন্য)

### আপনার প্রজেক্টের মূল `urls.py`-এ যুক্ত করুন:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # আপনার অন্যান্য URL patterns
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## ✅ ধাপ ৩: মডেলে media ফাইল ফিল্ড যুক্ত করুন

```python
from django.db import models

class StudentProfile(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
```

🔹 এখানে `upload_to='profile_pics/'` মানে ফাইলটা `media/profile_pics/` ফোল্ডারে যাবে।

---

## ✅ ধাপ ৪: ফর্মে মিডিয়া ফিল্ড যুক্ত করুন

### ফর্ম ক্লাসে:

```python
from django import forms
from .models import StudentProfile

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['name', 'profile_picture']
```

---

### ভিউতে:

```python
def create_profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = StudentProfileForm()
    return render(request, 'your_template.html', {'form': form})
```

> ⚠️ `request.FILES` না দিলে ফাইল সেভ হবে না।

---

### টেমপ্লেটে:

```html
<form method="post" enctype="multipart/form-data">
  {% csrf_token %} {{ form.as_p }}
  <button type="submit">Save</button>
</form>
```

> ⚠️ `enctype="multipart/form-data"` **অবশ্যই দিতে হবে**, না হলে ফাইল যাবে না।

---

## ✅ ধাপ ৫: মিডিয়া ফাইল টেমপ্লেটে দেখানো

```html
<img src="{{ student.profile_picture.url }}" alt="Profile Picture" />
```

> ⚠️ নিশ্চিত হোন আপনি `{% load static %}` এর মতো `{% load static %}` দিয়েই অন্যান্য ফাইল লোড করছেন।

---

## 📁 Folder Structure (Automatic after upload)

```
your_project/
├── media/
│   └── profile_pics/
│       └── uploaded_file.jpg
```

---

## 🔚 সংক্ষেপে:

| কাজ           | কোড                                                             |
| ------------- | --------------------------------------------------------------- |
| `settings.py` | `MEDIA_URL` ও `MEDIA_ROOT` যুক্ত করুন                           |
| `urls.py`     | `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` |
| মডেল          | `ImageField(upload_to=...)`                                     |
| ফর্ম          | `enctype="multipart/form-data"` এবং `request.FILES`             |
| টেমপ্লেট      | `{{ obj.image_field.url }}`                                     |

---

Django-তে **Login এবং Logout** করার জন্য Django নিজেই built-in authentication system দেয়, যেটা সহজ ও নিরাপদ। নিচে বাংলায় ধাপে ধাপে ব্যাখ্যা করছি।

---

## ✅ ধাপ ১: `urls.py`-এ login এবং logout URL যুক্ত করুন

Django-র built-in view ব্যবহার করতে চাইলে:

```python
from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
```

---

## ✅ ধাপ ২: `settings.py`-এ Login Redirect URL দিন

```python
# settings.py

LOGIN_REDIRECT_URL = '/'         # Login সফল হলে কোন পেইজে যাবে
LOGOUT_REDIRECT_URL = '/login/'  # Logout হলে কোথায় যাবে (বিকল্পভাবে view এ next_page ও দিতে পারেন)
```

---

## ✅ ধাপ ৩: Login টেমপ্লেট তৈরি করুন (`templates/login.html`)

```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
  </head>
  <body>
    <h2>Login</h2>
    {% if form.errors %}
    <p style="color:red;">Username or password incorrect!</p>
    {% endif %}
    <form method="post">
      {% csrf_token %} {{ form.as_p }}
      <button type="submit">Login</button>
    </form>
  </body>
</html>
```

---

## ✅ ধাপ ৪: লগআউট লিংক যুক্ত করুন

```html
<a href="{% url 'logout' %}">Logout</a>
```

---

## ✅ ধাপ ৫: শুধুমাত্র লগইন করা ইউজারকে কোনো পেইজ দেখাতে চাইলে

```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
```

> ⚠️ আপনি চাইলে class-based views-এ `LoginRequiredMixin` ব্যবহার করতে পারেন।

---

## ✅ অতিরিক্ত: নিজস্ব login/logout ভিউ তৈরি করতে চাইলে

```python
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def custom_logout(request):
    logout(request)
    return redirect('login')
```

---

## 🔚 সংক্ষেপে:

| কাজ           | কিভাবে করবেন                |
| ------------- | --------------------------- |
| Login view    | `LoginView.as_view()`       |
| Logout view   | `LogoutView.as_view()`      |
| নিজস্ব login  | `authenticate()`, `login()` |
| নিজস্ব logout | `logout()`                  |
| login রক্ষা   | `@login_required`           |

---
