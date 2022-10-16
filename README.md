# pulumi-github-repository
Pulumi automation code that manages the repositories in this GitHub organization

# Workflow at a glance

1. Anything on the `main` branch is deployable.
2. To work on something new, create a descriptively named branch off `main` (`git checkout -b <name>`)
3. Use one of the patterns below to make organization changes, make a commit.
4. Make sure the code is formatted properly with black and flake8.
5. Have a pull request already?
    - a. No: Make a pull request and fill in the pull request template (`gh pr create`)
    - b. Yes: Update the pull request
      - NOTE: If your push fails, you do not do a `git pull`. NEVER do a pull.
6. If approved, go to step 7. If changes requested, go to step 3.
7. Follow instructions on merging PRs below (`gh pr merge`)

## Adding a new engineering team repo

Engineering team repositories are read/write for the engineering team, read-only for other teams.
In `engineering_repositories.py` add a new entry to the `engineering_repositories` dictionary
in the following format - __maintain alphabetical ordering__!
```
engineering_repositories = {
    ....
    "<new_repo_name>": {
        "description": "<repo_description>"
    },
}

Example:
engineering_repositories = {
    ....
    "shiny": {
        "description": "A very shiny source code base"
    },
}
```

You can specify one special parameter, `farmonacci_access: True` for repos that need to be
accessed on the farmonacci test robot environment. Farmonacci 1.0 is not currently managed
through automation, so we're currently using a temporary bot credential plus an ssh key
for catkin to ensure read-only access in this environment. This setting should be
deprecated with Farmonacci 2.0 (and for any other robot environments, as we're not going
to set up any other environments by hand).

```
engineering_repositories = {
    ....
    "<new_repo_name>": {
        "description": "<repo_description>",
        "farmonacci_access": True,
    },
}

Example:
engineering_repositories = {
    ....
    "shiny_farmonacci": {
        "description": "A very shiny source code base that can be accessed on farmonacci",
        "farmonacci_access": True,
    },
}
```

# Renaming an existing repo

The name field is passed through to the child GitHub Repository resource in our
component resource abstraction. This controls the name of the GitHub repository.
To rename, keep the resource name the same, but change the name accordingly:
```
GitHubRepository(
    "caladan_examples",
    GitHubRepositoryArgs(
        name="caladan_examples_renamed",
        description="See your robot moving autonomously in simulation - today!",
        branch_protection_repository_id="R_kgDOIKLQbw",
    ),
)
```

```
% docker container run -it --rm \
    --env PULUMI_ACCESS_TOKEN \
    --workdir /app \
    --mount type=bind,source="$(pwd)",target=/app \
    --entrypoint bash \
    docker.io/polymathrobotics/pulumi-python
% pulumi stack select dev
% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/7551126f-b7a1-4baa-9de0-5c89e91b2cc2

     Type                              Name                                Plan
     pulumi:pulumi:Stack               pulumi-source-repository-dev-dev
     └─ polymath:scm:GitHubRepository  caladan_examples
 ~      └─ github:index:Repository     caladan_examples-github-repository

Resources:
    ~ 1 to update
    8 unchanged

% pulumi preview --diff
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/eb686b37-f458-4c0b-a21c-dc25e394a1c5

  pulumi:pulumi:Stack: (same)
    [urn=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:pulumi:Stack::pulumi-source-repository-dev-dev]
        ~ github:index/repository:Repository: (update) 🔒
            [id=caladan_examples]
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/repository:Repository::caladan_examples-github-repository]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::e6869289-675d-4f56-84ea-d0a2689d733c]
          ~ name: "caladan_examples" => "caladan_examples_renamed"
Resources:
    ~ 1 to update
    8 unchanged
root@79fb49b9af4b:/app# pulumi up
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/d6a51fcb-1e2d-4ef8-9e4c-b85962258a30

     Type                              Name                                Plan
     pulumi:pulumi:Stack               pulumi-source-repository-dev-dev
     └─ polymath:scm:GitHubRepository  caladan_examples
 ~      └─ github:index:Repository     caladan_examples-github-repository

Resources:
    ~ 1 to update
    8 unchanged

Do you want to perform this update?  [Use arrows to move, enter to select, type
Do you want to perform this update?  [Use arrows to move, enter to select, type
Do you want to perform this update? yes
Updating (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/updates/178

     Type                              Name                                Stat
     pulumi:pulumi:Stack               pulumi-source-repository-dev-dev
     └─ polymath:scm:GitHubRepository  caladan_examples
 ~      └─ github:index:Repository     caladan_examples-github-repository

Resources:
    ~ 1 updated
    8 unchanged

Duration: 4s

% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/aba33cf3-1eb9-4bb7-b2da-c2b7b8d0743c

     Type                 Name                              Plan
     pulumi:pulumi:Stack  pulumi-source-repository-dev-dev

Resources:
    9 unchanged
```

If you would also like to change the resource name, manually delete all state related to the
repository, then follow the procedure to import an existing repo. Unfortunately it looks like
using aliases to reparent/rename don't work with the terraform provider this support is based
on.

# Reformat code locally with black

```
$ docker run --rm \
    --mount type=bind,source="$(pwd)",target=/code \
    boxcutter/black .
```

# Importing an existing repo

Because we're using component resources that do not provide the ability to customize the import
workflow, you must adopt existing GitHub repositories via code, and not with "pulumi import".

You'll need to do some
interactive pulumi commands to import existing repositories, as in addition to performing
an import, normally the repo will need to be transition to have a standard repo setup as well.

Start by adding a reference to the repository with a name, description, and a repository_import
attribute. The `repository_import` attribute maps to the `import_` resource option. For more
information refer to https://www.pulumi.com/docs/guides/adopting/import/ Don't bother
adding it to one of the standard repo dictionaries just yet. Just add the reference to the end
of `__main__.py` as you'll likely need to modify it.

Also check if there is branch protection configured on the repo. If so, add an import for that
as well, by filling in the `branch_protection_*` attributes. You'll likely not know the
repository_id, so just use the repository name to start. Pulumi will supply that attribute
in a subsequent diff. You'll need to perform both the repository and branch protection imports
at the same time. The import won't work properly if you try to do them separately.

Here's an example of the source code changes for a repo named
`example` that also has branch protection configured:

```
from polymath.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "caladan_examples",
    GitHubRepositoryArgs(
        description="See your robot moving autonomously in simulation - today!",
        # This maps to _import
        repository_import="caladan_examples",
        # This maps to _import
        branch_protection_import="caladan_examples:main",
        branch_protection_pattern="main",
        branch_protection_repository_id='caladan_examples',
    ),
)
```

In most cases, you'll get a warning that the inputs do not match the existing resource(s)
when you run `pulumi preview`. To get more detail on which inputs differ, run 
`pulumi preview --diff`
```
$ docker container run -it --rm \
        --env PULUMI_ACCESS_TOKEN \
        --workdir /app \
        --mount type=bind,source="$(pwd)",target=/app \
        --entrypoint bash \
          docker.io/boxcutter/pulumi-python
% pulumi stack select org
% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/957548ab-50f9-4e93-9e99-e1c171bfe4c1

     Type                                 Name
     pulumi:pulumi:Stack                  pulumi-source-repository-dev-dev
 +   └─ polymath:scm:GitHubRepository     caladan_examples
 =      ├─ github:index:Repository        caladan_examples-github-repositor
 +      ├─ github:index:TeamRepository    caladan_examples-amazing-bot-gith
 +      ├─ github:index:TeamRepository    caladan_examples-infrastructure-g
 +      ├─ github:index:TeamRepository    caladan_examples-engineering-gith
 =      ├─ github:index:BranchProtection  caladan_examples-github-branch-pr
 +      ├─ github:index:BranchDefault     caladan_examples-github-branch-de
 +      └─ github:index:ActionsSecret     caladan_examples-ssh-private-key-

Diagnostics:
  github:index:BranchProtection (caladan_examples-github-branch-protection):
    warning: inputs to import do not match the existing resource; importing this resource will fail

  github:index:Repository (caladan_examples-github-repository):
    warning: inputs to import do not match the existing resource; importing this resource will fail


% pulumi preview --diff
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/04157d58-9083-48c0-b32f-ca9f0ca01e57

  pulumi:pulumi:Stack: (same)
    [urn=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:pulumi:Stack::pulumi-source-repository-dev-dev]
    + polymath:scm:GitHubRepository: (create)
        [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository::caladan_examples]
warning: inputs to import do not match the existing resource; importing this resource will fail
        = github:index/repository:Repository: (import) 🔒
            [id=caladan_examples]
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/repository:Repository::caladan_examples-github-repository]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
          ~ allowMergeCommit   : true => false
          ~ allowRebaseMerge   : true => false
          + archiveOnDestroy   : true
          ~ autoInit           : false => true
          ~ deleteBranchOnMerge: false => true
          ~ hasProjects        : false => true
          ~ hasWiki            : false => true
          + licenseTemplate    : "apache-2.0"
        + github:index/teamRepository:TeamRepository: (create)
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-amazing-bot-github-team-repository]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
            permission: "admin"
            repository: "caladan_examples"
            teamId    : "6366570"
        + github:index/teamRepository:TeamRepository: (create)
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-engineering-github-team-repository]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
            permission: "push"
            repository: "caladan_examples"
            teamId    : "6367064"
        + github:index/branchDefault:BranchDefault: (create)
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/branchDefault:BranchDefault::caladan_examples-github-branch-default]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
            branch    : "main"
            repository: "caladan_examples"
        + github:index/teamRepository:TeamRepository: (create)
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-infrastructure-github-team-repository]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
            permission: "push"
            repository: "caladan_examples"
            teamId    : "6367065"
        + github:index/actionsSecret:ActionsSecret: (create)
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/actionsSecret:ActionsSecret::caladan_examples-ssh-private-key-github-actions-secret]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
            plaintextValue: "superseekret"
            repository    : "caladan_examples"
            secretName    : "SSH_PRIVATE_KEY"
warning: inputs to import do not match the existing resource; importing this resource will fail
        = github:index/branchProtection:BranchProtection: (import) 🔒
            [id=BPR_kwDOIKLQb84BxXH7]
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/branchProtection:BranchProtection::caladan_examples-github-branch-protection]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::04da6b54-80e4-46f7-96ec-b56ff0331ba9]
          ~ repositoryId: "R_kgDOIKLQbw" => "caladan_examples"
Resources:
    + 6 to create
    = 2 to import
    8 changes. 1 unchanged
```

Add attributes as needed to match the values displayed in the diff. These are all the input
values for the pulumi GitHub provider Repository object: https://www.pulumi.com/registry/packages/github/api-docs/repository/
```
from polymath.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "caladan_examples",
    GitHubRepositoryArgs(
        description="See your robot moving autonomously in simulation - today!",
        repository_import="caladan_examples",
        allow_merge_commit = True,
        allow_rebase_merge = True,
        archive_on_destroy = None,
        auto_init = False,
        delete_branch_on_merge = False,
        has_projects = False,
        has_wiki = False,
        license_template = None,
        branch_protection_import="caladan_examples:main",
        branch_protection_pattern="main",
        branch_protection_repository_id='R_kgDOIKLQbw',
    ),
)
```

Iterate setting values until the preview no longer displays that the inputs to import do not match
the inputs to the existing resource.

```
% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/0aed8b21-b8bc-4ba9-a1c8-b83a56d7a6f7

     Type                                 Name
     pulumi:pulumi:Stack                  pulumi-source-repository-dev-dev
 +   └─ polymath:scm:GitHubRepository     caladan_examples
 =      ├─ github:index:Repository        caladan_examples-github-repositor
 +      ├─ github:index:TeamRepository    caladan_examples-amazing-bot-gith
 +      ├─ github:index:TeamRepository    caladan_examples-engineering-gith
 +      ├─ github:index:TeamRepository    caladan_examples-infrastructure-g
 +      ├─ github:index:BranchDefault     caladan_examples-github-branch-de
 =      ├─ github:index:BranchProtection  caladan_examples-github-branch-pr
 +      └─ github:index:ActionsSecret     caladan_examples-ssh-private-key-

Resources:
    + 6 to create
    = 2 to import
    8 changes. 1 unchanged

% pulumi up
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/6028ce4e-9c10-4d22-a7ed-c6070f6e8f87

     Type                                 Name
     pulumi:pulumi:Stack                  pulumi-source-repository-dev-dev
 +   └─ polymath:scm:GitHubRepository     caladan_examples
 =      ├─ github:index:Repository        caladan_examples-github-repositor
 +      ├─ github:index:TeamRepository    caladan_examples-amazing-bot-gith
 +      ├─ github:index:TeamRepository    caladan_examples-engineering-gith
 +      ├─ github:index:TeamRepository    caladan_examples-infrastructure-g
 =      ├─ github:index:BranchProtection  caladan_examples-github-branch-pr
 +      ├─ github:index:BranchDefault     caladan_examples-github-branch-de
 +      └─ github:index:ActionsSecret     caladan_examples-ssh-private-key-

Resources:
    + 6 to create
    = 2 to import
    8 changes. 1 unchanged

Do you want to perform this update?  [Use arrows to move, enter to select, type
Do you want to perform this update?  [Use arrows to move, enter to select, type
Do you want to perform this update? yes
Updating (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/updates/173

     Type                                 Name
     pulumi:pulumi:Stack                  pulumi-source-repository-dev-dev
 +   └─ polymath:scm:GitHubRepository     caladan_examples
 =      ├─ github:index:Repository        caladan_examples-github-repositor
 +      ├─ github:index:TeamRepository    caladan_examples-amazing-bot-gith
 +      ├─ github:index:TeamRepository    caladan_examples-engineering-gith
 +      ├─ github:index:ActionsSecret     caladan_examples-ssh-private-key-
 =      ├─ github:index:BranchProtection  caladan_examples-github-branch-pr
 +      ├─ github:index:BranchDefault     caladan_examples-github-branch-de
 +      └─ github:index:TeamRepository    caladan_examples-infrastructure-g

Resources:
    + 6 created
    = 2 imported
    8 changes. 1 unchanged

Duration: 17s

# A subsequent pulumi preview/up should display no resources changed:
% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/4d7f9819-4b67-4406-a751-09d967771120

     Type                 Name                              Plan
     pulumi:pulumi:Stack  pulumi-source-repository-dev-dev

Resources:
    9 unchanged
```

After successfully importing the resource, you can delete the import option attributes.
All subsequent operations will behave as though Pulumi provisioned the resource
from the outset:

```
GitHubRepository(
    "caladan_examples",
    GitHubRepositoryArgs(
        description="See your robot moving autonomously in simulation - today!",
        # repository_import="caladan_examples",
        allow_merge_commit = True,
        allow_rebase_merge = True,
        archive_on_destroy = None,
        auto_init = False,
        delete_branch_on_merge = False,
        has_projects = False,
        has_wiki = False,
        license_template = None,
        # branch_protection_import="caladan_examples:main",
        branch_protection_pattern="main",
        branch_protection_repository_id='R_kgDOIKLQbw',
    ),
)
```

Make sure preview reports that the resource is unchanged:

```
% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/4e49335b-1408-4c79-acc1-db1c160b8cb1

     Type                 Name                              Plan
     pulumi:pulumi:Stack  pulumi-source-repository-dev-dev

Resources:
    9 unchanged
```

Next you can start transitioning the repo to the standard inputs by deleting all the ones you
just added in the previous step. If you imported branch protection, the `repository_id` must
remain:
```
from polymath.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "caladan_examples",
    GitHubRepositoryArgs(
        description="See your robot moving autonomously in simulation - today!",
        # repository_import="caladan_examples",
        # allow_merge_commit = True,
        # allow_rebase_merge = True,
        # archive_on_destroy = None,
        # auto_init = False,
        # delete_branch_on_merge = False,
        # has_projects = False,
        # has_wiki = False,
        # license_template = None,
        # branch_protection_import="caladan_examples:main",
        # branch_protection_pattern="main",
        branch_protection_repository_id='R_kgDOIKLQbw',
    ),
)
```

When you apply the change you should see the repository just being updated, no removals. And then a subsequent
`pulumi up` should report no changes.
```
# pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/37bf0559-1eeb-4966-bbd1-6e07120226bc

     Type                              Name                                Plan
     pulumi:pulumi:Stack               pulumi-source-repository-dev-dev
     └─ polymath:scm:GitHubRepository  caladan_examples
 ~      └─ github:index:Repository     caladan_examples-github-repository

Resources:
    ~ 1 to update
    8 unchanged

# Should only update, not replace:

% pulumi preview --diff
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/35d5008f-3b49-41d2-b845-a737a3d9c861

  pulumi:pulumi:Stack: (same)
    [urn=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:pulumi:Stack::pulumi-source-repository-dev-dev]
        ~ github:index/repository:Repository: (update) 🔒
            [id=caladan_examples]
            [urn=urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/repository:Repository::caladan_examples-github-repository]
            [provider=urn:pulumi:dev::pulumi-source-repository-dev::pulumi:providers:github::default_5_0_0::e6869289-675d-4f56-84ea-d0a2689d733c]
          ~ allowMergeCommit   : true => false
          ~ allowRebaseMerge   : true => false
          + archiveOnDestroy   : true
          ~ autoInit           : false => true
          ~ deleteBranchOnMerge: false => true
          ~ hasProjects        : false => true
          ~ hasWiki            : false => true
          + licenseTemplate    : "apache-2.0"
Resources:
    ~ 1 to update
    8 unchanged

% pulumi up
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/5a785ef2-638f-4ad6-b36e-2038fcc200d2

     Type                              Name                                Plan
     pulumi:pulumi:Stack               pulumi-source-repository-dev-dev
     └─ polymath:scm:GitHubRepository  caladan_examples
 ~      └─ github:index:Repository     caladan_examples-github-repository

Resources:
    ~ 1 to update
    8 unchanged

Do you want to perform this update?  [Use arrows to move, enter to select, type
Do you want to perform this update?  [Use arrows to move, enter to select, type
Do you want to perform this update? yes
Updating (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/updates/174

     Type                              Name                                Stat
     pulumi:pulumi:Stack               pulumi-source-repository-dev-dev
     └─ polymath:scm:GitHubRepository  caladan_examples
 ~      └─ github:index:Repository     caladan_examples-github-repository

Resources:
    ~ 1 updated
    8 unchanged

Duration: 4s

# Should be unchanged after pulumi up

% pulumi preview
Previewing update (dev)

View Live: https://app.pulumi.com/beavertails/pulumi-source-repository-dev/dev/previews/93870dbf-773a-4247-9a89-09098a103156

     Type                 Name                              Plan
     pulumi:pulumi:Stack  pulumi-source-repository-dev-dev

Resources:
    9 unchanged
```

### Performing imports with the GitHub provider

If you need to troubleshoot an importing issue in the GitHub provider, you may need to try importing with 
the upstream non-custom resources in order to file an issue for support. This way you can rule out any
issues with our custom component.

```
# pulumi import github:index/repository:Repository <repo_name>_repository <repo_name>
# delete `private=True` - deprecated
# deploy to update state to set main branch

# pulumi import github:index/repository:Repository truck_sim_repository truck_sim
# pulumi import github:index/branchProtection:BranchProtection truck_sim_repository_branch_protection truck_sim:main
# pulumi import github:index/branchDefault:BranchDefault truck_sim_repository_branch_default truck_sim
# pulumi import github:index/teamRepository:TeamRepository truck_sim_repository_engineering_team_repository 5594486:truck_sim
# pulumi import github:index/teamRepository:TeamRepository truck_sim_repository_infrastructure_team_repository 5671481:truck_sim
# pulumi import github:index/teamRepository:TeamRepository truck_sim_repository_bot_team_repository 5594482:truck_sim
```

# Setting up the python virtual environment

```
$ docker container run -it --rm \
        --env PULUMI_ACCESS_TOKEN \
        --workdir /app \
        --mount type=bind,source="$(pwd)",target=/app \
        --entrypoint bash \
          docker.io/boxcutter/pulumi-python
# python3 -m venv venv  
# venv/bin/pip install -r requirements.txt
# python3 -m pip install --upgrade pip
# pulumi stack select org
```

## Manually deleting state:
```
% pulumi stack --show-urns
% pulumi state delete <resource URN>

% 
├─ polymath:scm:GitHubRepository                      caladan_examples
    │  │  URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository::caladan_examples
    │  ├─ github:index/repository:Repository              caladan_examples-github-repository
    │  │     URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/repository:Repository::caladan_examples-github-repository
    │  ├─ github:index/teamRepository:TeamRepository      caladan_examples-amazing-bot-github-team-repository
    │  │     URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-amazing-bot-github-team-repository
    │  ├─ github:index/teamRepository:TeamRepository      caladan_examples-engineering-github-team-repository
    │  │     URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-engineering-github-team-repository
    │  ├─ github:index/teamRepository:TeamRepository      caladan_examples-infrastructure-github-team-repository
    │  │     URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-infrastructure-github-team-repository
    │  ├─ github:index/branchDefault:BranchDefault        caladan_examples-github-branch-default
    │  │     URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/branchDefault:BranchDefault::caladan_examples-github-branch-default
    │  ├─ github:index/actionsSecret:ActionsSecret        caladan_examples-ssh-private-key-github-actions-secret
    │  │     URN: urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/actionsSecret:ActionsSecret::caladan_examples-ssh-private-key-github-actions-secret
    │  └─ github:index/branchProtection:BranchProtection  caladan_examples-github-branch-protection


# pulumi state delete 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/actionsSecret:ActionsSecret::caladan_examples-ssh-private-key-github-actions-secret'
 warning: This command will edit your stack's state directly. Confirm? Yes
Resource deleted

# pulumi state delete 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/branchDefault:BranchDefault::caladan_examples-github-branch-default'
 warning: This command will edit your stack's state directly. Confirm? Yes
Resource deleted

# pulumi state delete -y 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-infrastructure-github-team-repository'
Resource deleted

# pulumi state delete -y 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-engineering-github-team-repository'
Resource deleted

# pulumi state delete -y 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/teamRepository:TeamRepository::caladan_examples-amazing-bot-github-team-repository'
Resource deleted

# pulumi state delete -y 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/branchProtection:BranchProtection::caladan_examples-github-branch-protection'
Resource delete

# pulumi state delete -y 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/repository:Repository::caladan_examples-github-repository'
warning: A new version of Pulumi is available. To upgrade from version '3.41.1' to '3.42.0', visit https://pulumi.com/docs/reference/install/ for manual instructions and release notes.
error: This resource can't be safely deleted because it is protected. Re-run this command with --force to force deletion
root@f19a97a6c215:/app# pulumi state delete -y --force 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository$github:index/repository:Repository::caladan_examples-github-repository'
warning: deleting protected resource due to presence of --force
Resource deleted

# pulumi state delete -y 'urn:pulumi:dev::pulumi-source-repository-dev::polymath:scm:GitHubRepository::caladan_examples'
 warning: This command will edit your stack's state directly.
Resource deleted
```

# Setup

1. Use `PULUMI_ACCESS_TOKEN` for the boxcutter account ([1Password link](https://start.1password.com/open/i?a=ZCJFQ3OBFNBPZNZ4NB27WUYUBM&v=gt6zmthhtppympnyshkzmm26dq&i=utvu7uhmdoz33l4ap6uvjri3ei&h=sinagub.1password.com)

1. Create a new python project:

    ```bash
    $ docker container run -it --rm \
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

1. Provision the project:

    ```bash
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

1. Once you have provisioned a stack, you can get tips on how to integrate GitHub via the Pulumi CI/CD Integration Assistants. In the organization, navigate to the stack. Choose "Settings > Integrations". It will provide the latest link to the integration guide: https://www.pulumi.com/docs/guides/continuous-delivery/github-actions/

1. Install the Pulumi GitHub app wich will submit rich, inline comments on any pull request or commit: https://github.com/apps/pulumi

1. Add the PULUMI_ACCESS_TOKEN created earlier as a per-repository secret named `PULUMI_ACCESS_TOKEN`. This needs to be available to workflows in order to run pulumi non-interactively and so that the cli tool can communicate with the Pulumi service on your behalf.

1. Generate the CI/CD secret used to manage all the other repositories in the GitHub organization. Generate GitHub personal access token under the boxcutter account with `read:org` and `repo` permissions. Save in 1Password in the notes for the boxcutter account ([1Password link](https://start.1password.com/open/i?a=ZCJFQ3OBFNBPZNZ4NB27WUYUBM&v=gt6zmthhtppympnyshkzmm26dq&i=utvu7uhmdoz33l4ap6uvjri3ei&h=sinagub.1password.com) ).

1. Configure the CI/CD secret. Add GitHub personal access token to the Pulumi stack

    ```bash
    $ docker container run -it --rm \
        --env PULUMI_ACCESS_TOKEN \
        --workdir /app \
        --mount type=bind,source="$(pwd)",target=/app \
        --entrypoint bash \
          docker.io/boxcutter/pulumi-python
    % pulumi stack select org
    % pulumi config set github:owner boxcutter
    % pulumi config set --secret github:token <personal access token>
    ```

1. Wire up the pull_request workflow. Add a new file to the Pulumi project repository at `.github/workflows/pull_request.yml`:

    ```bash
    name: Pull request
    on:
      - pull_request
    jobs:
      preview:
        name: Preview
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3

          - name: Set up Python 3.8
            uses: actions/setup-python@v4
            with:
              python-version: 3.8

          - name: Install Pulumi packages
            run: |
                python3 -m venv venv
                venv/bin/pip install -r requirements.txt

          - name: Run pulumi preview
            uses: pulumi/actions@v3
            with:
              command: preview
              stack-name: org
              comment-on-pr: true
              github-token: ${{ secrets.GITHUB_TOKEN }}
            env:
              PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
    ```

1. Wire up the push workflow. Add a second file to the Pulumi project repository at `.github/workflows/push.yml`:

    ```bash
    name: Push
    on:
      push:
        branches:
          - main
    jobs:
      update:
        name: Update
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3

          - name: Set up Python 3.8
            uses: actions/setup-python@v4
            with:
              python-version: 3.8

          - name: Install Pulumi
            run: |
              python3 -m venv venv
              venv/bin/pip install -r requirements.txt

          - name: Run pulumi up
            uses: pulumi/actions@v3
            with:
              command: up
              stack-name: org
            env:
              PULUMI_ACCESS_TOKEN: ${{ secrets.PULUMI_ACCESS_TOKEN }}
    ```

1. Verify that the workflows behave correctly. Try creating pull requests and merge changes and iterate until everything works properly.

1. Refine the pipelines by adding the appropriate linters and formatters.

1. Make sure the following teams exist. These are used in assigning default permissions each repository:
     - amazing-bot
     - bot
     - contributor
     - maintainer

   Once the teams exist you'll need to add the team ids as config settings. You'll need to first dump the teams ids by running the following GitHub API command:

     ```bash
     # List team IDs
     GITHUB_API_TOKEN=<YOUR-TOKEN>
     curl \
       -H "Accept: application/vnd.github+json" \
       -H "Authorization: Bearer ${GITHUB_API_TOKEN}" \
       https://api.github.com/orgs/boxcutter/teams
     ```

    Once you have all the team IDs, create config entries for each similar to the following:

    ```bash
    $ docker container run -it --rm \
        --env PULUMI_ACCESS_TOKEN \
        --workdir /app \
        --mount type=bind,source="$(pwd)",target=/app \
        --entrypoint bash \
          docker.io/boxcutter/pulumi-python
    # pulumi stack select org
    # pulumi config set boxcutter:amazing_bot_team_id 6809378
    # pulumi config set boxcutter:bot_team_id 6809380
    # pulumi config set boxcutter:contributor_team_id 6809383
    # pulumi config set boxcutter:maintainer_team_id 6809382
    ```
