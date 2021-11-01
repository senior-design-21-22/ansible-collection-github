# Ansible Collection for GitHub

### The OHIO IT collection of Ansible modules for GitHub.

The collection includes a variety of Ansible modules to help automate the management of organizations, repositories, and user permissions in GitHub.

---

## Version Compatibility

Tested against:
`Ansible Version >=2.11`
`Python >=3.8`
`PyGitHub >=1.55`

## Installation

Install this collection via [Ansible Galaxy](https://galaxy.ansible.com/ohioit/github):

```bash
ansible-galaxy collection install ohioit.github
```

Content in this collection requires the [PyGitHub package](https://github.com/PyGithub/PyGithub) to interact with [GitHub REST API](https://docs.github.com/en/rest). You can install it with:

```bash
pip install PyGithub
```

## Included Content

### Modules

| Name                                                                                                                                             | Description                                                                            |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| [repository_information](https://github.com/senior-design-21-22/ansible-collection-github/blob/development/docs/repository_information.rst) | Output repositories along with vital information from an (user specified) organization |
| [collaborator_information](https://github.com/senior-design-21-22/ansible-collection-github/blob/development/docs/collaborator_information.rst) | View and manage repository collaborators |

## Usage

### Repository Information (From organization)

```
  - name: "List GitHub repositories within non-enterprise org"
    ohioit.github.repository_information:
      token: "[token]"
      organization_name: "[org name]"
    register: result

  - name: "List GitHub repositories within enterprise org"
    ohioit.github.repository_information:
      token: "[token]"
      organization_name: "[org name]"
      enterprise_url: "https://github.ohio.edu/your/url/here/"
    register: result     
```
### Collaborator Information (From organization)

```
    - name: "Some functions of Collaborator informationm module"
      ohioit.github.collaborator_information:
        token: "[token]"
        organization_name: "[org name]"
        enterprise_url: "https://github.ohio.edu/your/url/here/"
        repos:
          - "[repo 1]"
          - "[repo 2]"
          - "[repo 3]"
        collaborators_to_add:
          [GitHub username]: "[triage, pull, push or admin]"
        check_collaborator:
          [GitHub username]: "[triage, pull, push or admin]"
        collaborators_to_change:
          [GitHub username]: "[triage, pull, push or admin]"
        collaborators_to_remove:
          - "[GitHub username]"   
```

###### _**NOTE**: Tokens should be encrypted and only decrypted at runtime_

## Testing with 'ansible-test'

Testing has been made available using the [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html). These tests include [unit](https://github.com/senior-design-21-22/ansible-collection-github/blob/development/docs/unit_testing.rst), [sanity](https://github.com/senior-design-21-22/ansible-collection-github/tree/repo-information-module/unit/sanity), [integration](https://github.com/senior-design-21-22/ansible-collection-github/blob/development/docs/integration_testing.rst).

The tests are runnable using the following commands:

```bash
ansible-test units --python 3.[YOUR PYTHON VERSION] --venv
ansible-test sanity
ansible-test integration
```
