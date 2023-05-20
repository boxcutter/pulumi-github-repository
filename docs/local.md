# Setup

1. Use `PULUMI_ACCESS_TOKEN` for boxcutter@jpfm.dev.

```
# Install the 1Password CLI and connect the 1Password app to the
# 1Password CLI.
#   https://developer.1password.com/docs/cli/get-started
op signin
# op item get 'Pulumi (boxcutter@jpfm.dev)' --vault boxcutter
# op item get utvu7uhmdoz33l4ap6uvjri3ei --format json
export PULUMI_ACCESS_TOKEN=$(op read 'op://Boxcutter/utvu7uhmdoz33l4ap6uvjri3ei/credential')
```

1. Blah
```
docker container run -it --rm \
--env PULUMI_ACCESS_TOKEN \
--workdir /app \
--mount type=bind,source="$(pwd)",target=/app \
--entrypoint bash \
docker.io/boxcutter/pulumi-python
```