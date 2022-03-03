# resan-api

Using python 3.10
Poetry
FastAPI
Pymongo
Heroku

Link to [Resan UI](https://github.com/fitzypop/resan-ui).

Link to [Shared Resan Repo](https://github.com/fitzypop/resan).

## Set poetry buildpack for heroku

<https://github.com/moneymeets/python-poetry-buildpack>

```shell
heroku buildpacks:clear
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
```

make sure the buildpack in the dashboard makes the order above.
