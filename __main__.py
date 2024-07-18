"""Manage boxcutter org"""

import pulumi_github
from boxcutter.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "bootstrap-chef",
    GitHubRepositoryArgs(
        description="JEOS images for bootstrapping Chef",
    ),
)
GitHubRepository(
    "bsd",
    GitHubRepositoryArgs(
        description="Virtual machine templates for BSD flavours written in legacy JSON",
    ),
)
GitHubRepository(
    "boxcutter-chef-cookbooks",
    GitHubRepositoryArgs(
        description="Boxcutter Chef automation",
    ),
)
GitHubRepository(
    "centos",
    GitHubRepositoryArgs(
        description="Virtual machine templates for CentOS written in legacy JSON",
    ),
)
GitHubRepository(
    "container-build-publish-action",
    GitHubRepositoryArgs(
        description="GitHub Action to build and publish container images with Buildx.",
    ),
)
GitHubRepository(
    "debian",
    GitHubRepositoryArgs(
        description="Virtual machine templates for Debian written in legacy JSON",
    ),
)
GitHubRepository(
    "esxi",
    GitHubRepositoryArgs(
        description="Virtual machine templates for ESXi, the VMware bare-metal hypervisor written legacy JSON",
    ),
)
GitHubRepository(
    "fedora",
    GitHubRepositoryArgs(
        description="Virtual machine templates for Fedora written in legacy JSON",
    ),
)
GitHubRepository(
    "go2chef",
    GitHubRepositoryArgs(
        description="A Golang tool to bootstrap a system from zero so that it's able to run Chef to be managed ",
    ),
)
GitHubRepository(
    "kvm",
    GitHubRepositoryArgs(
        description="Packer templates for producing KVM images written in HCL",
    ),
)
GitHubRepository(
    "macos",
    GitHubRepositoryArgs(
        description="Virtual machine templates for macOS written in legacy JSON",
    ),
)
GitHubRepository(
    "oci",
    GitHubRepositoryArgs(
        description="Open container images 📦",
        override_repository_args=pulumi_github.RepositoryArgs(
            homepage_url="https://hub.docker.com/u/boxcutter",
            topics=["neuroinformatics", "robotics", "docker", "podman", "container"],
        ),
    ),
)
GitHubRepository(
    "oraclelinux",
    GitHubRepositoryArgs(
        description="Virtual machine templates for Oracle Linux written in legacy JSON",
    ),
)
GitHubRepository(
    "sles",
    GitHubRepositoryArgs(
        description="SUSE Linux Enterprise Server templates written in legacy JSON",
    ),
)
GitHubRepository(
    "syscheck",
    GitHubRepositoryArgs(
        description="InSpec system validation scripts",
    ),
)
GitHubRepository(
    "ubuntu",
    GitHubRepositoryArgs(
        description="Virtual machine templates for Ubuntu written in legacy JSON",
    ),
)
GitHubRepository(
    "virtualbox",
    GitHubRepositoryArgs(
        description="Packer templates for producing Oracle VM VIrtualBox images written in HCL",
    ),
)
GitHubRepository(
    "windows",
    GitHubRepositoryArgs(
        description="Virtual machine templates for Windows written in legacy JSON and Batch Scripting/JScript",
    ),
)
GitHubRepository(
    "windows-ps",
    GitHubRepositoryArgs(
        description="Experimental Windows templates written in legacy JSON based on PowerShell scripts",
    ),
)
