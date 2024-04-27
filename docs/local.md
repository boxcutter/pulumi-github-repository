# Working locally

Usually performed by core team members to import repositories or manage state:

1. Use `PULUMI_ACCESS_TOKEN` for `boxcutter`.

```
# Install the 1Password CLI and connect the 1Password app to the
# 1Password CLI.
#   https://developer.1password.com/docs/cli/get-started
op signin
# op item get 'PULUMI_ACCESS_TOKEN (boxcutter) local workflow' --vault Infrastructure
# op item get maqd4zbl3crlsnnjwfbek5ic54 --vault Infrastructure --format json
export PULUMI_ACCESS_TOKEN=$(op read 'op://Infrastructure/maqd4zbl3crlsnnjwfbek5ic54/credential')
```

1. Use the pulumi-python container image to run pulumi commands:
```
$ docker container run -it --rm \
    --env PULUMI_ACCESS_TOKEN \
    --workdir /app \
    --mount type=bind,source="$(pwd)",target=/app \
    --entrypoint bash \
    docker.io/boxcutter/pulumi-python
% python3 -m venv venv  
% venv/bin/pip install -r requirements.txt
% python3 -m pip install --upgrade pip
% pulumi stack select org
# <enter in pulumi commands here>
```
