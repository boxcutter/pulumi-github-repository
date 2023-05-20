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

1. Create a new python project:
   ```
   docker container run -it --rm \
     --env PULUMI_ACCESS_TOKEN \
     --workdir /app \
     --mount type=bind,source="$(pwd)",target=/app \
     --entrypoint bash \
     docker.io/boxcutter/pulumi-python \
       -c "pulumi new python \
           --stack org \
           --name pulumi-github-repository \
           --description 'Manage GitHub repositories in the boxcutter org with pulumi'"
   ```

1. Generate the CI/CD secret used to manage all the other repositories in the
   GitHub organization. Generate a GitHub personal access token under the
   `amazing-flowers` account with the `repo` and `read:org` permissions.
   ```
   op item create \
     --category='API Credential' \
     --title='boxcutter pulumi-github-repository GitHub personal access token' \
     --vault='Boxcutter' \
     username='amazing-flowers' \
     credential='ghp_<token>' \
     validFrom='2023-05-20' \
     expires='2023-08-18'
   ```

1. Add the GitHub personal access token to the Pulumi stack:
   ```
   pulumi stack select org
   pulumi config set github:owner boxcutter
   op read 'op://Boxcutter/boxcutter pulumi-github-repository GitHub personal access token/credential' \
     | pulumi config set github:token --secret 
   ```
   
1. Provision the project:
   ```
   $ docker container run -it --rm \
     --env PULUMI_ACCESS_TOKEN \
     --workdir /app \
     --mount type=bind,source="$(pwd)",target=/app \
     --entrypoint bash \
     docker.io/boxcutter/pulumi-python
   % pulumi stack select org
   % pulumi preview
   % pulumi up
   ```