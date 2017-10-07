# blog

Blog is an application django and extension a baseapp

### Prerequisites

* **django**

```
pip3 install Django
```
or
```
pip install Django
```

and install **[baseapp](https://github.com/Nelestya/baseapp)**



## Getting Started
add your file settings project the application baseapp
and add urls.py in your project

```
urlpatterns = [
    url(r'^/blog', include('blog.urls')),
    ]
```

and use this command

```
python3 manage.py makemigrations
python3 manage.py migrate
``` 

## Motivation
The goal is to create a website and the ability to learn and easily modify it

## Installation

```
git clone https://github.com/Nelestya/blog.git
```

## Authors
* **Dlugosz Tristan** - *Initial work* - [blog](https://github.com/Nelestya/blog)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Nelestya/blog/blob/master/LICENSE) file for details
