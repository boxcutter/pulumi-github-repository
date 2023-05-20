import pulumi
import pulumi_github


class GitHubBranchProtectionArgs:
    def __init__(
        self,
        name="main",
        override_branch_protection_args: pulumi_github.BranchProtectionArgs = None,
        import_: str = None,
    ):
        self.name = name
        self.override_branch_protection_args = override_branch_protection_args
        self.import_ = import_


class GitHubRepositoryArgs:
    def __init__(
        self,
        description: str = None,
        default_branch: str = "main",
        amazing_bot_team_permission="admin",
        bot_team_permission=None,
        contributor_team_permission="push",
        maintainer_team_permission="push",
        repository_import: str = None,
        override_repository_args: pulumi_github.RepositoryArgs = None,
        branch_protection_import=None,
        branch_protection_pattern="main",
        branch_protection_repository_id=None,
    ):
        self.description = description
        self.default_branch = default_branch
        self.branch_protection_import = branch_protection_import
        self.branch_protection_pattern = branch_protection_pattern
        self.branch_protection_repository_id = branch_protection_repository_id
        self.amazing_bot_team_permission = amazing_bot_team_permission
        self.bot_team_permission = bot_team_permission
        self.contributor_team_permission = contributor_team_permission
        self.maintainer_team_permission = maintainer_team_permission
        self.repository_import = repository_import
        self.override_repository_args = override_repository_args


class GitHubRepository(pulumi.ComponentResource):
    # Set defaults and overrides for the Repository resource
    def __check_repository_args(self, name: str, args: GitHubRepositoryArgs):
        repository_args = pulumi_github.RepositoryArgs(
            allow_auto_merge=False,
            allow_merge_commit=False,
            allow_rebase_merge=False,
            allow_squash_merge=True,
            archive_on_destroy=True,
            auto_init=True,
            delete_branch_on_merge=True,
            has_downloads=True,
            has_issues=True,
            has_projects=True,
            has_wiki=True,
            license_template="apache-2.0",
            name=name,
            description=args.description,
            visibility="public",
            vulnerability_alerts=True,
        )

        # Handle override defaults for import
        if args.repository_import is not None:
            if args.override_repository_args is None:
                # Even though we always set these properties on create, they seem to
                # get unset when we drop state and re-import (guess these things aren't
                # queryable through the api). So populate them by default.
                args.override_repository_args = pulumi_github.RepositoryArgs(
                    archive_on_destroy=...,
                    auto_init=False,
                    license_template=...,
                )

        if args.override_repository_args is not None:
            override_repository_args_dict = args.override_repository_args.__dict__
            for key, value in override_repository_args_dict.items():
                # Sometimes it will be necessary to unset one of the settings
                # we set at default above to import.
                # Since it's not possible to check if an optional parameter comes
                # its default value or because it has been set explicitly, the
                # user indicates this by using Ellipses.
                if value is ...:
                    setattr(repository_args, key, None)
                else:
                    setattr(repository_args, key, value)

        return repository_args

    # Set defaults and overrides for the BranchProtection resource
    def __check_branch_protection_args(
        self,
        args: GitHubBranchProtectionArgs,
        pulumi_github_repository_args: pulumi_github.RepositoryArgs,
    ):
        branch_protection_args = pulumi_github.BranchProtectionArgs(
            pattern=args.name,
            repository_id=pulumi_github_repository_args.name,
        )

        if args.import_ is not None:
            if args.override_branch_protection_args is None:
                github_repository = pulumi_github.get_repository(
                    full_name=f"boxcutter/{pulumi_github_repository_args.name}"
                )
                branch_protection_args = pulumi_github.BranchProtectionArgs(
                    pattern=args.name, repository_id=github_repository.node_id
                )

        if args.override_branch_protection_args is not None:
            override_branch_protection_args_dict = (
                args.override_branch_protection_args.__dict__
            )
            for key, value in override_branch_protection_args_dict.items():
                # Sometimes it will be necessary to unset one of the settings
                # we set at default above to import.
                # Since it's not possible to check if an optional parameter comes
                # its default value or because it has been set explicitly, the
                # user indicates this by using Ellipses.
                if value is ...:
                    setattr(branch_protection_args, key, None)
                else:
                    setattr(branch_protection_args, key, value)

        return branch_protection_args

    def __init__(
        self, name, args: GitHubRepositoryArgs, opts: pulumi.ResourceOptions = None
    ):
        super().__init__("boxcutter:scm:GitHubRepository", name, {}, opts)

        config = pulumi.Config("boxcutter")

        amazing_bot_team_id = config.require("amazing_bot_team_id")
        bot_team_id = config.require("bot_team_id")
        maintainer_team_id = config.require("maintainer_team_id")
        contributor_team_id = config.require("contributor_team_id")

        repository_args = self.__check_repository_args(name, args)

        self.github_repository = pulumi_github.Repository(
            f"{name}-github-repository",
            args=repository_args,
            opts=pulumi.ResourceOptions(
                protect=True,
                parent=self,
                import_=args.repository_import,
            ),
        )

        pulumi_github.TeamRepository(
            f"{name}-amazing-bot-github-team-repository",
            permission=args.amazing_bot_team_permission,
            repository=name,
            team_id=amazing_bot_team_id,
            opts=pulumi.ResourceOptions(
                depends_on=[self.github_repository],
                parent=self,
            ),
        )

        if args.bot_team_permission is not None:
            pulumi_github.TeamRepository(
                f"{name}-bot-github-team-repository",
                permission=args.bot_team_permission,
                repository=name,
                team_id=bot_team_id,
                opts=pulumi.ResourceOptions(
                    depends_on=[self.github_repository],
                    parent=self,
                ),
            )

        pulumi_github.TeamRepository(
            f"{name}-maintainer-github-team-repository",
            permission=args.maintainer_team_permission,
            repository=name,
            team_id=maintainer_team_id,
            opts=pulumi.ResourceOptions(
                depends_on=[self.github_repository],
                parent=self,
            ),
        )

        pulumi_github.TeamRepository(
            f"{name}-contributor-github-team-repository",
            permission=args.contributor_team_permission,
            repository=name,
            team_id=contributor_team_id,
            opts=pulumi.ResourceOptions(
                depends_on=[self.github_repository],
                parent=self,
            ),
        )

        pulumi_github.BranchDefault(
            f"{name}-github-branch-default",
            branch="main",
            repository=name,
            opts=pulumi.ResourceOptions(
                depends_on=[self.github_repository],
                parent=self,
            ),
        )

        pulumi_github.BranchProtection(
            f"{name}-github-branch-protection",
            pattern="main"
            if args.branch_protection_pattern is None
            else args.branch_protection_pattern,
            repository_id=name
            if args.branch_protection_repository_id is None
            else args.branch_protection_repository_id,
            opts=pulumi.ResourceOptions(
                protect=True,
                depends_on=[self.github_repository],
                parent=self,
            ),
        )

        self.register_outputs({})
