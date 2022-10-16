"""Manage boxcutter org"""

from boxcutter.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "sles",
    GitHubRepositoryArgs(
        description="SUSE Linux Enterprise Server templates written in legacy JSON",
    ),
)
GitHubRepository(
    "windows-ps",
    GitHubRepositoryArgs(
        description="Experimental Windows templates written in legacy JSON based on PowerShell scripts",
    ),
)

# GitHubRepository(
#     "sles",
#     GitHubRepositoryArgs(
#         description = "SUSE Linux Enterprise Server templates written in legacy JSON",
#         repository_import="sles",
#         allow_merge_commit = True,
#         allow_rebase_merge = True,
#         archive_on_destroy = None,
#         auto_init = False,
#         delete_branch_on_merge = False,
#         license_template = None,
#     ),
# )
