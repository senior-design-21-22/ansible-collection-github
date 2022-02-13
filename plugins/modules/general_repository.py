#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import collections
from email.policy import default
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from github import Github
from numpy import outer
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: repository_information

short_description: A module that returns information about GitHub repositories

description:
  - "A module that fetches information about repositories that a GitHub user has access to inside an organization."

options:
    token:
        description:
            - GitHub API token used to retrieve information about repositories to which a user has access to
        required: true
        type: str
    enterprise_url:
        description:
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL.
              This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>'.
        required: false
        type: str
    organization_name:
        description:
          - The organization in which the query will be run.
        required: true
        type: str

author:
    - Jacob Eicher (@jacobeicher)
    - Bradley Golski (@bgolski)
    - Tyler Zwolenik (@TylerZwolenik)
    - Nolan Khounborinn (@Khounborinn)
'''

EXAMPLES = '''
# Pass in an organization name and GitHub API token
- name: returns information about
  repository_webhooks:
    organization: "senior-design-21-22"
    github_token: "12345"


# Pass in an organization name, GitHub API token and enterprise URL
- name: returns information about
  repository_info:
    organization: "SSEP"
    github_token: "12345"
    enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>"
'''

RETURN = '''
webhooks:
    description: List contains dictionaries of webhooks and their information.
    type: list
    returned: if GitHub API token connects

repos.<ELEMENT INDEX>:
    description: Dictionary contains keys and values of a repository's information.
    type: dict
    returned: only if at least one repo is contained within organization

'''


# def check_repo_name(g, organization, repo):
#     org = g.get_organization("org-name")


def run_module():
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo_name=dict(type='str', default=''),
        team_id=dict(type='int', default=0),
        private=dict(type='bool', default=False),
        has_issues=dict(type='bool', default=False),
        has_wiki=dict(type='bool', default=False),
        auto_init=dict(type='bool', default=False),
        has_downloads=dict(type='bool', default=False),
        has_projects=dict(type='bool', default=False),
        allow_squash_merge=dict(type='bool', default=False),
        allow_merge_commit=dict(type='bool', default=False),
        allow_rebase_merge=dict(type='bool', default=False),
        delete_branch_on_merge=dict(type='bool', default=False),
        description=dict(type='str', default=''),
        homepage=dict(type='str', default=''),
        license_template=dict(type='str', default=''),
        gitignore_template=dict(type='str', default=''),
        state=dict(type='str', default='present'),
    )

    valid_states = ["absent", "present"]

    valid_licenses = ["afl-3.0",
                      "apache-2.0",
                      "artistic-2.0",
                      "bsl-1.0",
                      "bsd-2-clause",
                      "bsd-3-clause",
                      "bsd-3-clause-clear",
                      "cc",
                      "cc0-1.0",
                      "cc-by-4.0",
                      "cc-by-sa-4.0",
                      "wtfpl",
                      "ecl-2.0",
                      "epl-1.0",
                      "epl-2.0",
                      "eupl-1.1",
                      "agpl-3.0",
                      "gpl",
                      "gpl-2.0",
                      "gpl-3.0",
                      "lgpl",
                      "lgpl-2.1",
                      "lgpl-3.0",
                      "isc",
                      "lppl-1.3c",
                      "ms-pl",
                      "mit",
                      "mpl-2.0",
                      "osl-3.0",
                      "postgresql",
                      "ofl-1.1",
                      "ncsa",
                      "unlicense",
                      "zlib"]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.params['enterprise_url'] == '':
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'],
                   base_url=module.params['enterprise_url'])

    try:
        repo = g.get_organization(
            module.params['organization_name']).get_repo(module.params['repo_name'])
        initial = {
            "name": repo.name,
            "full_name": repo.full_name,
            "owner": repo.owner.login,
            "description": repo.description,
            "private": repo.private,
            "archived": repo.archived,
            "language": repo.language,
            "url": repo.url,
            "default_branch": repo.default_branch,
            "hooks_url": repo.hooks_url,
            "clone_url": repo.clone_url
        }
    except Exception as e:
        with open("/Users/bradleygolski/Desktop/ansibleOutput.txt", "w+") as temp:
            temp.write("made it here\n")
        initial = {}

    # with open("/Users/bradleygolski/Desktop/ansibleOutput.txt", "w+") as temp:
    #     for team in g.get_organization(module.params['organization_name']).get_teams():
    #         temp.write(str(team))
    #         temp.write("\n")

    if module.params['state'] == 'present':
        try:
            repo = g.get_organization(module.params['organization_name']).get_repo(
                module.params['repo_name'])
            if repo:
                with open("/Users/bradleygolski/Desktop/ansibleOutput2.txt", "w+") as temp:
                    temp.write("repo exists")
                repo.edit(name=module.params['repo_name'],
                          description=module.params['description'],
                          homepage=module.params['homepage'],
                          private=module.params['private'],
                          has_issues=module.params['has_issues'],
                          has_projects=module.params['has_projects'],
                          has_wiki=module.params['has_wiki'],
                          has_downloads=module.params['has_downloads'],
                          allow_squash_merge=module.params['allow_squash_merge'],
                          allow_merge_commit=module.params['allow_merge_commit'],
                          allow_rebase_merge=module.params['allow_rebase_merge'],
                          delete_branch_on_merge=module.params['delete_branch_on_merge'])
        except Exception as e:
            # if not check_repo_name(g, module.params['organization_name'], module.params['repo_name']):
            g.get_organization(module.params['organization_name']).create_repo(
                module.params['repo_name'],
                module.params['description'],
                module.params['homepage'],
                module.params['private'],
                module.params['has_issues'],
                module.params['has_wiki'],
                module.params['has_downloads'],
                module.params['has_projects'],
                module.params['team_id'],
                module.params['auto_init'],
                module.params['license_template'],
                module.params['gitignore_template'],
                module.params['allow_squash_merge'],
                module.params['allow_merge_commit'],
                module.params['allow_rebase_merge'],
                module.params['delete_branch_on_merge']
            )

    repo = g.get_organization(
        module.params['organization_name']).get_repo(module.params['repo_name'])

    output = {
        "name": repo.name,
        "full_name": repo.full_name,
        "owner": repo.owner.login,
        "description": repo.description,
        "private": repo.private,
        "archived": repo.archived,
        "language": repo.language,
        "url": repo.url,
        "default_branch": repo.default_branch,
        "hooks_url": repo.hooks_url,
        "clone_url": repo.clone_url
    }

    with open("/Users/bradleygolski/Desktop/ansibleOutput.txt", "w+") as temp:
        temp.write(str(initial))
        temp.write("\n")
        temp.write(str(output))

    result = dict(
        changed=collections.Counter(initial) != collections.Counter(output)
    )

    if module.check_mode:
        return result

    module.exit_json(repos=output)


def main():
    run_module()


if __name__ == '__main__':
    main()
