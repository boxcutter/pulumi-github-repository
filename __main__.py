"""A Python Pulumi program"""

import pulumi

from boxcutter.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "windows-ps",
    GitHubRepositoryArgs(
        description="Experimental Windows templates written in legacy JSON based on PowerShell scripts",
    ),
)
