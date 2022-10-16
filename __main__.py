"""A Python Pulumi program"""

from boxcutter.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "windows-ps",
    GitHubRepositoryArgs(
        description="Experimental Windows templates written in legacy JSON based on PowerShell scripts",
    ),
)
