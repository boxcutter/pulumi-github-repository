import pulumi
import pulumi_github


class GitHubRepositoryArgs:
    def __init__(
        self,
        # All the input parameters for the pulumi Repository Resource
        allow_auto_merge=False,
        allow_merge_commit=False,
        allow_rebase_merge=False,
        allow_squash_merge=True,
        archive_on_destroy=True,
        archived=None,
        auto_init=True,
        delete_branch_on_merge=True,
        description=None,
        gitignore_template=None,
        has_downloads=True,
        has_issues=True,
        has_projects=True,
        has_wiki=True,
        homepage_url=None,
        ignore_vulnerability_alerts_during_read=None,
        is_template=None,
        license_template="apache-2.0",
        merge_commit_message=None,
        merge_commit_title=None,
        name=None,
        pages=None,
        squash_merge_commit_message=None,
        squash_merge_commit_title=None,
        template=None,
        topics=None,
        visibility="public",
        vulnerability_alerts=True,
        repository_import=None,
        branch_protection_import=None,
        branch_protection_pattern="main",
        branch_protection_repository_id=None,
        amazing_bot_team_permission="admin",
        bot_team_permission=None,
        contributor_team_permission="push",
        maintainer_team_permission="push",
    ):
        self.allow_auto_merge = allow_auto_merge
        self.allow_merge_commit = allow_merge_commit
        self.allow_rebase_merge = allow_rebase_merge
        self.allow_squash_merge = allow_squash_merge
        self.archive_on_destroy = archive_on_destroy
        self.archived = archived
        self.auto_init = auto_init
        self.delete_branch_on_merge = delete_branch_on_merge
        self.description = description
        self.gitignore_template = gitignore_template
        self.has_downloads = has_downloads
        self.has_issues = has_issues
        self.has_projects = has_projects
        self.has_wiki = has_wiki
        self.homepage_url = homepage_url
        self.ignore_vulnerability_alerts_during_read = (
            ignore_vulnerability_alerts_during_read
        )
        self.is_template = is_template
        self.license_template = license_template
        self.merge_commit_message = merge_commit_message
        self.merge_commit_title = merge_commit_title
        self.name = name
        self.pages = pages
        self.squash_merge_commit_message = squash_merge_commit_message
        self.squash_merge_commit_title = squash_merge_commit_title
        self.template = template
        self.topics = topics
        self.visibility = visibility
        self.vulnerability_alerts = vulnerability_alerts
        self.repository_import = repository_import
        self.branch_protection_import = branch_protection_import
        self.branch_protection_pattern = branch_protection_pattern
        self.branch_protection_repository_id = branch_protection_repository_id
        self.amazing_bot_team_permission = amazing_bot_team_permission
        self.bot_team_permission = bot_team_permission
        self.contributor_team_permission = contributor_team_permission
        self.maintainer_team_permission = maintainer_team_permission


class GitHubRepository(pulumi.ComponentResource):
    def __init__(
        self, name, args: GitHubRepositoryArgs, opts: pulumi.ResourceOptions = None
    ):
        super().__init__("boxcutter:scm:GitHubRepository", name, {}, opts)

        config = pulumi.Config("boxcutter")

        amazing_bot_team_id = config.require("amazing_bot_team_id")
        bot_team_id = config.require("amazing_bot_team_id")
        maintainer_team_id = config.require("maintainer_team_id")
        contributor_team_id = config.require("contributor_team_id")

        repository_name = args.name
        if repository_name is None:
            repository_name = name

        if args.repository_import is None:
            self.github_repository = pulumi_github.Repository(
                f"{name}-github-repository",
                allow_auto_merge=args.allow_auto_merge,
                allow_merge_commit=args.allow_merge_commit,
                allow_rebase_merge=args.allow_rebase_merge,
                allow_squash_merge=args.allow_squash_merge,
                archive_on_destroy=args.archive_on_destroy,
                archived=args.archived,
                auto_init=args.auto_init,
                delete_branch_on_merge=args.delete_branch_on_merge,
                description=args.description,
                gitignore_template=args.gitignore_template,
                has_downloads=args.has_downloads,
                has_issues=args.has_issues,
                has_projects=args.has_projects,
                has_wiki=args.has_wiki,
                homepage_url=args.homepage_url,
                ignore_vulnerability_alerts_during_read=args.ignore_vulnerability_alerts_during_read,
                is_template=args.is_template,
                license_template=args.license_template,
                merge_commit_message=args.merge_commit_message,
                merge_commit_title=args.merge_commit_title,
                name=repository_name,
                pages=args.pages,
                squash_merge_commit_message=args.squash_merge_commit_message,
                squash_merge_commit_title=args.squash_merge_commit_title,
                template=args.template,
                topics=args.topics,
                visibility=args.visibility,
                vulnerability_alerts=args.vulnerability_alerts,
                opts=pulumi.ResourceOptions(protect=True, parent=self),
            )
        else:
            self.github_repository = pulumi_github.Repository(
                f"{name}-github-repository",
                allow_auto_merge=args.allow_auto_merge,
                allow_merge_commit=args.allow_merge_commit,
                allow_rebase_merge=args.allow_rebase_merge,
                allow_squash_merge=args.allow_squash_merge,
                archive_on_destroy=args.archive_on_destroy,
                archived=args.archived,
                auto_init=args.auto_init,
                delete_branch_on_merge=args.delete_branch_on_merge,
                description=args.description,
                gitignore_template=args.gitignore_template,
                has_downloads=args.has_downloads,
                has_issues=args.has_issues,
                has_projects=args.has_projects,
                has_wiki=args.has_wiki,
                homepage_url=args.homepage_url,
                ignore_vulnerability_alerts_during_read=args.ignore_vulnerability_alerts_during_read,
                is_template=args.is_template,
                license_template=args.license_template,
                merge_commit_message=args.merge_commit_message,
                merge_commit_title=args.merge_commit_title,
                name=repository_name,
                pages=args.pages,
                squash_merge_commit_message=args.squash_merge_commit_message,
                squash_merge_commit_title=args.squash_merge_commit_title,
                template=args.template,
                topics=args.topics,
                visibility=args.visibility,
                vulnerability_alerts=args.vulnerability_alerts,
                opts=pulumi.ResourceOptions(
                    protect=True, parent=self, import_=args.repository_import
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

        if args.branch_protection_import is None:
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
        else:
            pulumi_github.BranchProtection(
                f"{name}-github-branch-protection",
                pattern=args.branch_protection_pattern,
                repository_id=args.branch_protection_repository_id,
                opts=pulumi.ResourceOptions(
                    protect=True,
                    depends_on=[self.github_repository],
                    parent=self,
                    import_=args.branch_protection_import,
                ),
            )

        self.register_outputs({})
