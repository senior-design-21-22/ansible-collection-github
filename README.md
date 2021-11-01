# Ansible Collection for GitHub
### The OHIO IT collection of Ansible modules for GitHub.
The collection includes a variety of Ansible modules to help automate the management of organizations, repositories, and user permissions in GitHub.

---
## Version Compatibility
Tested against:
  ```Ansible Version >=2.11```
  ```Python >=3.8```
  ```PyGitHub >=1.55```
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
Name | Description
--- | ---
[repository_info](https://github.com/senior-design-21-22/ansible-collection-github/blob/repo-information-module/docs/repository_information.rst)|Output repositories along with vital information from an (user specified) organization

## Usage

### Repository Information (From organization)
```    
  - name: "List GitHub repositories within org"
      import_role:
        name: ohioit.github.repository_info
      vars:
        github_token: "token"
        org_name: "organization_name"
```
###### *__NOTE__: Tokens should be encrypted and only decrypted at runtime*


## Testing with 'ansible-test'
Testing has been made available using the [ansible-test](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html). These tests include [unit](https://github.com/senior-design-21-22/ansible-collection-github/tree/repo-information-module/tests/unit), [sanity](https://github.com/senior-design-21-22/ansible-collection-github/tree/repo-information-module/unit/sanity), integration. 

The tests are runnable using the following commands:
```bash
ansible-test unit
ansible-test sanity
ansible-test integration
```


