"""Manage boxcutter org"""

from boxcutter.scm.github import GitHubRepository, GitHubRepositoryArgs

GitHubRepository(
    "bsd",
    GitHubRepositoryArgs(
        description="Virtual machine templates for BSD flavours written in legacy JSON",
    ),
)
GitHubRepository(
    "centos",
    GitHubRepositoryArgs(
        description="Virtual machine templates for CentOS written in legacy JSON",
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
        homepage_url="https://hub.docker.com/u/boxcutter",
        topics=["neuroinformatics", "robotics", "docker", "podman", "container"],
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
