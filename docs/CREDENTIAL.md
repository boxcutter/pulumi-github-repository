1. Add the GitHub personal access token to the Pulumi stack:
   ```
   # op item get 'pulumi-github-repository GitHub token blue' --vault Automation-Org
   # op item get g5zsnmm34jph67hoxktfeo57gm --vault Automation-Org --format json
   # op read 'op://Automation-Org/pulumi-github-repository GitHub token blue/credential'
   pulumi stack select org
   pulumi config set github:owner boxcutter
   op read 'op://Automation-Org/pulumi-github-repository GitHub token blue/credential' \
     | pulumi config set github:token --secret
   ```

## 1Password Service account

```
# op item get 'Service Account Auth Token: automation-org-readonly-blue' --vault Automation-Org
# op item get mzqlddelxv6oe7dfz3vc7iad7m --format json
pulumi stack select org
op read 'op://Automation-Org/mzqlddelxv6oe7dfz3vc7iad7m/credential' | \
  pulumi config set op:service_account_token --non-interactive --secret
```
