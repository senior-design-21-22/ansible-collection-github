#!/usr/bin/python

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
            - If using a token from a GitHub Enterprise account, the user must pass an enterprise URL. This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3/repos/<ORGANIZATION NAME>/<REPO NAME>'.
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
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from github import Github
from ansible.module_utils.basic import AnsibleModule
def get_webhooks(g,repo_list):
    hooks = []
    for repo in repo_list:
        for current_hook in g.get_repo(repo).get_hooks():
            current_hook_dict = {}
            current_hook_dict = {
                "id": current_hook.id,
                "name": current_hook.name,
                "url": current_hook.url,
                "active": current_hook.active,
                "test_url": current_hook.test_url,
                "ping_url": current_hook.ping_url
            
        }
        hooks.append(current_hook_dict)
    output = [i for n, i in enumerate(hooks) if i not in hooks[n + 1:]]

    return output
def run_module():
    module_args = dict(
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(type='str', default='No Organization Name Provided.'),
        enterprise_url=dict(type='str', default=''),
        repos=dict(type='list', elements='str')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result = dict(
        changed=False,
        fact=''
    )
    if(module.params['enterprise_url'] == ''):
        g = Github(module.params['token'])
    else:
        g = Github(module.params['token'], base_url=module.params['enterprise_url'])
        
    if len(module.params['repos']):
        for i in range(len(module.params['repos'])):
            module.params['repos'][i] = module.params['organization_name'] + "/" + module.params['repos'][i]
        
    output=get_webhooks(g,module.params['repos'])
    if module.check_mode:
        return result

    module.exit_json(webhooks=output)



def main():
    run_module()

if __name__ == '__main__':
    main()
