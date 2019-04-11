# Cyber Hygiene API 🎛🎚

[![Total alerts](https://img.shields.io/lgtm/alerts/g/cisagov/cyhy-api.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/cyhy-api/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cisagov/cyhy-api.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/cyhy-api/context:python)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/cisagov/cyhy-api.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cisagov/cyhy-api/context:javascript)

This project implements the CyHy API used by the
[CyHy web client](https://github.com/cisagov/cyhy-web).

## Requirements

A working [Docker](https://docker.com) environment.

## Running

### Development

Start up the docker containers with the development container composition:

`docker-compose -f docker-compose-dev.yml up`

This will create:

- the API server with a [GraphiQL](https://github.com/graphql/graphiql) interface
available at [http://localhost:5000/graphql](http://localhost:5000/graphql)
- a [MongoDB](https://mongodb.com) server (no ports mapped to host)
- a [Mongo Express](https://github.com/mongo-express/mongo-express) web client
to view the database avaiable at [http://localhost:8081](http://localhost:8081)

### Testing

System and unit tests can be run using the debug container composition:

`docker-compose -f docker-compose-debug.yml run test`

[Extra arguments](https://docs.pytest.org/en/latest/usage.html) can be passed to
`pytest` by appending them to the command.

e.g.; `docker-compose -f docker-compose-debug.yml run test -vs`

A `bash` shell can be invoked using:
`docker-compose -f docker-compose-debug.yml run bash`

### Production

A production version of the server can be deployed to a
[swarm](https://docs.docker.com/engine/swarm/stack-deploy/) using:

`docker stack deploy --compose-file docker-compose.yml cyhy-api`

Note that the `config_yml` and `flask_key` secrets must be defined using
the `docker secret` command.  For example:

`docker secret create config_yml tests/secrets/config-mock.yml`

`docker secret create flask_key tests/secrets/flask.key`
