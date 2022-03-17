#!/usr/bin/python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


def absent_branch_protection(g, repo, branch):
    branch = g.get_repo(repo).get_branch(branch)
    branch.remove_protection()


def absent_branch_protection_check_mode():
    output = dict()
    return output

def present_branch_protection_check_mode(initial, branch_protections, api_url, repository, organization, branch):
    if initial != {}:
        output = initial.copy()
    else:
        output = {
            "allow_deletions": {
                "enabled": False
            },
            "allow_force_pushes": {
                "enabled": False
            },
            "enforce_admins": {
                "enabled": False,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/enforce_admins"
            },
            "required_conversation_resolution": {
                "enabled": False
            },
            "required_linear_history": {
                "enabled": False
            },
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": False,
                "dismissal_restrictions": {
                    "teams": [],
                    "teams_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions/teams",
                    "url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions",
                    "users": [],
                    "users_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions/users"
                },
                "require_code_owner_reviews": False,
                "required_approving_review_count": 0,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/required_pull_request_reviews"
            },
            "required_signatures": {
                "enabled": False,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/required_signatures"
            },
            "required_status_checks": {
                "contexts": [],
                "contexts_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/required_status_checks/contexts",
                "strict": False,
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/S" + organization + "SEP/" + repository + "/branches/" + branch + "/protection/required_status_checks"
            },
            "restrictions": {
                "apps": [],
                "apps_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/restrictions/apps",
                "teams": [],
                "teams_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/restrictions/teams",
                "url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/restrictions",
                "users": [],
                "users_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/restrictions/users"
            },
            "url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection"
        }
        
    output['enforce_admins']['enabled'] = branch_protections['enforce_admins']
    output['required_pull_request_reviews']['dismiss_stale_reviews'] = branch_protections['dismiss_stale_reviews'] 
    output['required_status_checks']['strict'] = branch_protections['strict']
    output['required_status_checks']['contexts'] = branch_protections['contexts']
    output['required_pull_request_reviews']['dismiss_stale_reviews'] = branch_protections['dismiss_stale_reviews']
    output['required_pull_request_reviews']['require_code_owner_reviews'] = branch_protections['require_code_owner_reviews']
    output['required_pull_request_reviews']['required_approving_review_count'] = branch_protections['required_approving_review_count']

    for team in branch_protections["dismissal_teams"]:
        if next((x for x in output['required_pull_request_reviews']['dismissal_restrictions']['teams'] if x["name"] == team), None) == None:
            new_team = {
                        "description": "This is a team to test branch protection functionality",
                        "html_url": "https://" + (api_url if api_url else "github.com") + "/repos/" + organization + "/" + repository + "/branches/" + branch + "/protection/dismissal_restrictions/teams",
                        "id": 0,
                        "members_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/members{/member}",
                        "name": team,
                        "node_id": "NodeID",
                        "parent": None,
                        "permission": "pull",
                        "privacy": "closed",
                        "repositories_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/repos",
                        "slug": team,
                        "url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0"
                    }
            output['required_pull_request_reviews']['dismissal_restrictions']['teams'].append(new_team)
    
    for team in output['required_pull_request_reviews']['dismissal_restrictions']['teams']:
        if team['name'] not in branch_protections['dismissal_teams']:
            output['required_pull_request_reviews']['dismissal_restrictions']['teams'].remove(team)
            
            
    for user in branch_protections["dismissal_users"]:
        if next((x for x in output['required_pull_request_reviews']['dismissal_restrictions']['users'] if x["login"] == user), None) == None:
            new_user = {
                        "avatar_url": "https://avatars." + (api_url if api_url else "github.com") + "/u/108?",
                        "events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/events{/privacy}",
                        "followers_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/followers",
                        "following_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/following{/other_user}",
                        "gists_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/gists{/gist_id}",
                        "gravatar_id": "",
                        "html_url": "https://" + (api_url if api_url else "github.com") + "/" + user,
                        "id": 000,
                        "login": user,
                        "node_id": "NodeID",
                        "organizations_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/orgs",
                        "received_events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/received_events",
                        "repos_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/repos",
                        "site_admin": False,
                        "starred_url": "https://" + (api_url if api_url else "github.com") + "//users/" + user + "/starred{/owner}{/repo}",
                        "subscriptions_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/subscriptions",
                        "type": "User",
                        "url": "https://" + (api_url if api_url else "github.com") + "/users/" + user
                    }
            output['required_pull_request_reviews']['dismissal_restrictions']['users'].append(new_user)

    for user in output['required_pull_request_reviews']['dismissal_restrictions']['users']:
        if user['login'] not in branch_protections['dismissal_users']:
            output['required_pull_request_reviews']['dismissal_restrictions']['users'].remove(user)
            
    for team in branch_protections["team_push_restrictions"]:
        if next((x for x in output['restrictions']['teams'] if x["name"] == team), None) == None:
            new_team={
                        "description": "This is a team to test branch protection functionality",
                        "html_url": "https://" + (api_url if api_url else "github.com") + "/orgs/" + organization + "/teams/" + team,
                        "id": 0,
                        "members_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/members{/member}",
                        "name": team,
                        "node_id": "NodeID",
                        "parent": None,
                        "permission": "pull",
                        "privacy": "closed",
                        "repositories_url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0/repos",
                        "slug": team,
                        "url": "https://" + (api_url if api_url else "github.com") + "/organizations/0/team/0"
                    }
            output['restrictions']['teams'].append(new_team)

    for team in output['restrictions']['teams']:
        if team['name'] not in branch_protections['team_push_restrictions']:
            output['restrictions']['teams'].remove(team)

    for user in branch_protections["user_push_restrictions"]:
        if next((x for x in output['restrictions']['users'] if x["login"] == user), None) == None:
            new_user ={
                        "avatar_url": "https://" + (api_url if api_url else "github.com") + "/u/0",
                        "events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/events{/privacy}",
                        "followers_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/followers",
                        "following_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/following{/other_user}",
                        "gists_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/gists{/gist_id}",
                        "gravatar_id": "",
                        "html_url": "https://" + (api_url if api_url else "github.com") + "/" + user,
                        "id": 0,
                        "login": user,
                        "node_id": "NodeID",
                        "organizations_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/orgs",
                        "received_events_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/received_events",
                        "repos_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/repos",
                        "site_admin": False,
                        "starred_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/starred{/owner}{/repo}",
                        "subscriptions_url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + "/subscriptions",
                        "type": "User",
                        "url": "https://" + (api_url if api_url else "github.com") + "/users/" + user + ""
                    }
            output['restrictions']['users'].append(new_user)

    for user in output['restrictions']['users']:
        if user['login'] not in branch_protections['user_push_restrictions']:
            output['restrictions']['users'].remove(user)

    return output


def present_branch_protections(g, repo, branch, branch_protections):
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
        access_token=dict(type='str', required=True, no_log=True),
        organization=dict(
            type='str', required=True),
        api_url=dict(type='str'),
        repository=dict(type='str', required=True),
        branch=dict(type='str', required=True),
        branch_protections=dict(type='dict'),
        state=dict(type="str", default="present")
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if(module.params['api_url'] == ''):
        g = Github(module.params['access_token'])
    else:
        g = Github(module.params['access_token'],
                   base_url=module.params['api_url'])

    if len(module.params['repository']):
        module.params['repository'] = module.params['organization'] + \
            "/" + module.params['repository']

    initial = get_branch_protections(g, module.params['repository'], module.params['branch'], module.params['access_token'])
    output = dict()
    if not initial:
        initial = {}

    if module.params["state"] == "present":
        if module.check_mode:
            output = present_branch_protection_check_mode(initial, module.params['branch_protections'], module.params['api_url'], module.params['repository'], module.params['organization'], module.params['branch'])
        else:
            present_branch_protections(g, module.params['repository'], module.params['branch'], module.params['branch_protections'])

    if module.params["state"] == "absent":
        if module.check_mode:
            output = absent_branch_protection_check_mode()
        else:
            absent_branch_protection(g, module.params['repository'], module.params['branch'])

    if module.check_mode == False:
        output = get_branch_protections(g, module.params['repository'], module.params['branch'], module.params['access_token'])

    result = dict(
        changed=initial != output,
        fact=''
    )


    module.exit_json(branch_protections=output, changed=initial != output)


def main():
    run_module()


if __name__ == '__main__':
    main()
