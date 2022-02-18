
#!/usr/bin/python

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: branch_protection

short_description: A module that allows the modification of branch protections.

description:
  - "A module that allows the addition, deletion and modification of existing branch protections"

options:
    token:
        description:
            - GitHub API token used to retrieve information about repositories to which a user has access.
        required: true
        type: str
    enterprise_url:
        description:
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL. This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3'.
        required: false
        type: str
    organization_name:
        description:
          - The organization in which branch protections will be modified.
        required: true
        type: str
    repo:
        description:
          - The repository in which branch protections will be modified.
        required: true
        type: str
    branch:
        description:
          - The branch whose protections will be modified.
        required: true
        type: str
    state:
        description:
          - When provided 'present', the branch protection will either be created of modified. When provided 'absent', the branch protection will be deleted.
        required: true
        type: str
    branch_protections:
        description:
          - The following elements will be modified or created upon the state being 'present'.
        required: false
        type: dict
    strict:
        description:
          - The branch must be up to date with the base branch before merging.
        required: false
        type: bool
    contexts:
        description:
          - The list of status checks to require in order to merge into this branch.
        required: false
        type: list
    enforce_admins:
        description:
          - Set to 'true' to enforce required status checks for repository administrators.
        required: false
        type: bool
    dismissal_users:
        description:
          - Specify which users can dismiss pull request reviews.
        required: false
        type: list
    dismissal_teams:
        description:
          - Specify which teams can dismiss pull request reviews.
        required: false
        type: list
    dismiss_stale_reviews:
        description:
          - Set to true if you want to automatically dismiss approving reviews when someone pushes a new commit.
        required: false
        type: bool
    require_code_owner_reviews:
        description:
          - Blocks merging pull requests until code owners have reviewed.
        required: false
        type: bool
    required_approving_review_count:
        description:
          - Specifies the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.
        required: false
        type: int
    user_push_restrictions:
        description:
          - Restrict who can push to the protected branch. User restrictions are only available for organization-owned repositories.
        required: false
        type: list
    team_push_restrictions:
        description:
          - Restrict who can push to the protected branch. Team restrictions are only available for organization-owned repositories.
        required: false
        type: list

author:
    - Jacob Eicher (@jacobeicher)
    - Bradley Golski (@bgolski)
    - Tyler Zwolenik (@TylerZwolenik)
    - Nolan Khounborinn (@Khounborinn)
'''

EXAMPLES = '''
# Given an existing branch, create or modify current branch protections
- name: "Modify branch protections to a branch"
  ohioit.github.branch_protection:
    token: "12345"
    organization_name: "SSEP"
    enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
    repo: "testing-repo-public"
    branch: "tyler-branch"
    state: present
    branch_protections:
      strict: false
      contexts: ["default", "ci-test"]
      enforce_admins: false
      dismissal_users: ["nk479217", "bg881717"]
      dismissal_teams: ["tyler-team"]
      dismiss_stale_reviews: false
      require_code_owner_reviews: true
      required_approving_review_count: 5
      user_push_restrictions: ["nk479217"]
      team_push_restrictions: ["tyler-team"]
    register: result

# Remove the current branch protections on the branch provided
- name: "Remove all branch protections from a branch"
  ohioit.github.branch_protection:
    token: "12345"
    organization_name: "SSEP"
    enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
    repo: "testing-repo-public"
    branch: "tyler-branch"
    state: absent
    register: result
'''

RETURN = '''
branch_protections:
    description: Dictionary describing branch protections of a single branch.
    type: dict
    returned: If branch provided is valid.

branch_protections.allow_deletions.enabled:
    description: Allows deletions within the branch.
    type: bool
    returned: If branch protections are present.

branch_protections.allow_force_pushes.enabled:
    description: Allows force pushes within the branch.
    type: bool
    returned: If branch protections are present.

branch_protections.enforce_admins.enabled:
    description: Enforce all configured restrictions for administrators. Set to true to enforce required status checks for repository administrators.
    type: bool
    returned: If branch protections are present.
    
branch_protections.enforce_admins.url:
    description: API URL where to find the enforce_admins status
    type: str
    returned: If branch protections are present.

branch_protections.required_conversation_resolution.enabled:
    description: Requires all conversations on code to be resolved before a pull request can be merged into a branch that matches this rule. Set to false to disable.
    type: bool
    returned: If branch protections are present.

branch_protections.required_linear_history.enabled:
    description: Enforces a linear commit Git history, which prevents anyone from pushing merge commits to a branch. Set to true to enforce a linear commit history. Set to false to disable a linear commit Git history. Your repository must allow squash merging or rebase merging before you can enable a linear commit history.
    type: bool
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.dismiss_stale_reviews:
    description: Set to true if you want to automatically dismiss approving reviews when someone pushes a new commit.
    type: bool
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.dismissal_restrictions.teams:
    description: Specifies which teams can dismiss pull request reviews.
    type: list
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.dismissal_restrictions.teams_url:
    description: API URL to access the dismissal restriction teams.
    type: str
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.dismissal_restrictions.url:
    description: API URL to access the dismissal restrictions.
    type: str
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.dismissal_restrictions.users:
    description: List of user dictionaries and their information
    type: list
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.dismissal_restrictions.users_url:
    description: API URL access to the users with dismissal restrictions
    type: str
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.require_code_owner_reviews:
    description: Blocks merging pull requests until code owners have reviewed.
    type: bool
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.required_approving_review_count:
    description: Specifies the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.
    type: int
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.required_approving_review_count:
    description: Specifies the number of reviewers required to approve pull requests. Use a number between 1 and 6 or 0 to not require reviewers.
    type: int
    returned: If branch protections are present.

branch_protections.required_pull_request_reviews.url:
    description: URL to access required pull request reviews.
    type: str
    returned: If branch protections are present.

branch_protections.required_signatures.enabled:
    description: Status of whether signatures are required.
    type: bool
    returned: If branch protections are present.

branch_protections.required_signatures.url:
    description: URL to access status of whether signatures are required.
    type: bool
    returned: If branch protections are present.

branch_protections.required_status_checks.contexts:
    description: The list of status checks to require in order to merge into this branch.
    type: list
    returned: If branch protections are present.

branch_protections.required_status_checks.contexts:
    description: The list of status checks to require in order to merge into this branch.
    type: list
    returned: If branch protections are present.

branch_protections.required_status_checks.contexts_url:
    description: The URL where to find the list of status checks to require in order to merge into this branch.
    type: str
    returned: If branch protections are present.

branch_protections.restrictions.apps:
    description: list of apps that restrict who can push to the protected branch.
    type: list
    returned: If branch protections are present.

branch_protections.restrictions.apps_url:
    description: URL where to find the list of apps that restrict who can push to the protected branch.
    type: str
    returned: If branch protections are present.

branch_protections.restrictions.teams:
    description: list of teams that restrict who can push to the protected branch.
    type: list
    returned: If branch protections are present.

branch_protections.restrictions.teams_url:
    description: URL where to find the list of teams that restrict who can push to the protected branch.
    type: str
    returned: If branch protections are present.

branch_protections.restrictions.users:
    description: list of users that restrict who can push to the protected branch.
    type: list
    returned: If branch protections are present.

branch_protections.restrictions.users_url:
    description: URL where to find the list of users that restrict who can push to the protected branch.
    type: str
    returned: If branch protections are present.

branch_protections.restrictions.url:
    description: URL where to find branch protection restrictions
    type: str
    returned: If branch protections are present.

branch_protections.url:
    description: URL where to find branch protections
    type: str
    returned: If branch protections are present.
'''

from github import Github
from ansible.module_utils.common.text.converters import jsonify
from ansible.module_utils.basic import AnsibleModule
import json
import collections
import requests


def remove_branch_protection(g, repo, branch):
    branch = g.get_repo(repo).get_branch(branch)
    branch.remove_protection()


def edit_branch_protections(g, repo, branch, branch_protections):
    try:
        branch = g.get_repo(repo).get_branch(branch)
        branch.edit_protection(strict=branch_protections["strict"],
                               contexts=branch_protections["contexts"],
                               enforce_admins=branch_protections["enforce_admins"],
                               dismissal_users=branch_protections["dismissal_users"],
                               dismissal_teams=branch_protections["dismissal_teams"],
                               dismiss_stale_reviews=branch_protections["dismiss_stale_reviews"],
                               require_code_owner_reviews=branch_protections["require_code_owner_reviews"],
                               required_approving_review_count=branch_protections["required_approving_review_count"],
                               user_push_restrictions=branch_protections["user_push_restrictions"],
                               team_push_restrictions=branch_protections["team_push_restrictions"])

    except Exception as e:
        return e


def get_branch_protections(g, repo, branch, token):
    output = {}
    try:
        branch = g.get_repo(repo).get_branch(branch)
        if not branch.protected:
            return output
        else:
            url = branch.protection_url
            output = requests.get(url, headers={'Authorization': 'Bearer {}'.format(token)}).json()
            return output

    except Exception as e:
        return e


def run_module():
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo=dict(type='str', default='No Repo Provided.'),
        branch=dict(type='str', default='No Branch Provided.'),
        branch_protections=dict(type='dict'),
        state=dict(type="str", default="No State Provided.")
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if(module.params['enterprise_url'] == ''):
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'],
                   base_url=module.params['enterprise_url'])

    if len(module.params['repo']):
        module.params['repo'] = module.params['organization_name'] + \
            "/" + module.params['repo']

    initial = get_branch_protections(g, module.params['repo'], module.params['branch'], module.params['token'])
    if not initial:
        initial = {}

    if module.params["branch_protections"] and module.params["state"] == "present":
        edit_branch_protections(g, module.params['repo'], module.params['branch'], module.params['branch_protections'])

    if module.params["state"] == "absent":
        remove_branch_protection(g, module.params['repo'], module.params['branch'],)

    output = get_branch_protections(g, module.params['repo'], module.params['branch'], module.params['token'])
    if not output:
        output = {}
    result = dict(
        changed=initial != output,
        fact=''
    )

    if module.check_mode:
        return result

    module.exit_json(branch_protections=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()
