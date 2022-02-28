#!/usr/bin/python

from __future__ import absolute_import, division, print_function
import collections
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from github import Github

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
module: repository_webhooks

short_description: A module that manages webhooks

description:
  - "A module that manages a repository's webhooks by adding, deleting, and editing."

options:
    token:
        description:
            - GitHub API token used to retrieve information about repositories to which a user has access.
        required: true
        type: str
    enterprise_url:
        description:
            - If using a GitHub API token from a GitHub Enterprise account, the user must pass an enterprise URL.
              This URL must be structured as 'https://github.<ENTERPRISE DOMAIN>/api/v3'.
        required: false
        type: str
    organization_name:
        description:
          - The organization in which the query will be run.
        required: true
        type: str
    action:
        description:
          - The current task's purpose. This can be to "add", "delete", or "edit".
        required: false
        type: str
    repo:
        description:
          - The provided repository will have its webhooks modified
        required: true
        type: str
    url:
        description:
          - The provided url will be the webhook that is added, deleted, or edited. This must be structured as <SCHEME(https://)><HOST(fakewebsite.com)><ENDPOINT(/path/end/here)>
        required: false
        type: str
    events:
        description:
          - The list of provided events will be added to what triggers a webhook. The following events are valid "branch_protection_rule", "check_run", "check_suite", "code_scanning_alert", "commit_comment", "content_reference", "create", "delete", "deploy_key", "deployment", "deployment_status", "discussion", "discussion_comment", "fork", "github_app_authorization", "gollum", "installation", "installation_repositories", "issue_comment", "issues", "label", "marketplace_purchase", "member", "membership", "meta", "milestone", "organization", "org_block", "package", "page_build", "ping", "project_card", "project_column", "project", "public", "pull_request", "pull_request_review", "pull_request_review_comment", "push", "release", "repository_dispatch", "repository", "repository_import", "repository_vulnerability_alert", "secret_scanning_alert", "security_advisory", "sponsorship", "star", "status", "team", "team_add", "watch", "workflow_dispatch", or "workflow_job". This is used with the "add" action.
        required: false
        type: list
    content_type:
        description:
          - The provided content type will be the webhook's primary content type. This can either be "json" or "form". The set default of an arguement is not provided is "json". This is used with the "add" action.
        required false
        type: str
    active_status:
        description:
          - This sets the active status of the webhook depending on whether it is provided "true" or "false". This is used in "edit" action.
        required: false
        type: string
    add_events:
        description:
          - When provided a list of events to add, the provided url of the webhook will recieve the additions. This is used in "edit" action.
        required: false
        type: list
    remove_events:
        description:
          - When provided a list of events to remove, the provided url of the webhook will remove the events. This is used in "edit" action.
        required: false
        type: list
    new_url:
        description:
          - Given a url, the current webhook will be update to the new url. This is used in "edit" action.
        required: false
        type: list
    new_content_type:
        description:
          - Given a content type, the current webhook will be update to the new content type. This is used in "edit" action.
        required: false
        type: string

author:
    - Jacob Eicher (@jacobeicher)
    - Bradley Golski (@bgolski)
    - Tyler Zwolenik (@TylerZwolenik)
    - Nolan Khounborinn (@Khounborinn)
"""

EXAMPLES = """
- name: "LIST WEBHOOK OF REPOSITORY"
    ohioit.github.repository_webhooks:
      token: "<TOKEN>"
      organization_name: "<ORG NAME>"
      enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
      repo: "<REPOSITORY NAME>"
    register: result

- name: "ADD WEBHOOK TO REPOSITORY"
    ohioit.github.repository_webhooks:
      action: "add"
      token: "<TOKEN>"
      organization_name: "<ORG NAME>"
      enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
      repo: "<REPOSITORY NAME>"
      url: <SCHEME("https://")><HOST("fakewebsite.com")><ENDPOINT("/path/end/here")>
      content_type: "json"
      events:
        - "public"
        - "push"
    register: result

- name: "EDIT WEBHOOK IN REPOSITORY"
    ohioit.github.repository_webhooks:
      action: "edit"
      token: "<TOKEN>"
      organization_name: "<ORG NAME>"
      enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
      repo: "<REPOSITORY NAME>"
      url: "<SCHEME(https://)><HOST(fakewebsite.com)><ENDPOINT(/path/end/here)>"
      add_events:
        - "create"
      remove_events:
        - "public"
      new_url: "<SCHEME(https://)><HOST(newfakewebsite.com)><ENDPOINT(/path/end/there)>"
    register: result
    
- name: "REMOVE WEBHOOK IN GITHUB REPOSITORY"
    ohioit.github.repository_webhooks:
    action: "delete"
      token: "<TOKEN>"
      organization_name: "<ORG NAME>"
      enterprise_url: "https://github.<ENTERPRISE DOMAIN>/api/v3"
      repo: "<REPOSITORY NAME>"
      url: "<SCHEME(https://)><HOST(fakewebsite.com)><ENDPOINT(/path/end/here)>"
    register: result
"""

RETURN = """
webhooks:
    description: List contains dictionaries of webhooks and their information.
    type: list
    returned: if GitHub API token connects

webhooks.<ELEMENT INDEX>:
    description: Dictionary contains keys and values of webhooks' information.
    type: dict
    returned: if at least one webhook is contained within organization

webhooks.<ELEMENT INDEX>.active:
    description: Status of whether the webhook is active or not.
    type: bool
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.config:
    description: dictionary containing the webhook's content type, insecure ssl number, and the url of where to send.
    type: dict
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.config.content_type:
    description: The format of the webhook being sent to the url.
    type: str
    returned: provided per webhook's configuration

webhooks.<ELEMENT INDEX>.config.insecure_ssl:
    description: The status of the website being sent information. Whether or not it is secure (https vs http).
    type: str
    returned: provided per webhook's configuration

webhooks.<ELEMENT INDEX>.config.url:
    description: The url that the webhook is sending to.
    type: str
    returned: provided per webhook's configuration

webhooks.<ELEMENT INDEX>.events:
    description: List of events that trigger the webhook to send data.
    type: list
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.id:
    description: Unique identifier for the webhook in the repository.
    type: int
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.name:
    description: Name of the webhook.
    type: string
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.ping_url:
    description: The url to ping the webhook.
    type: string
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.test_url:
    description: The url to test the webhook.
    type: string
    returned: provided per webhook dictionary

webhooks.<ELEMENT INDEX>.url:
    description: The url in which the webhook resides
    type: string
    returned: provided per webhook dictionary
"""


def get_webhooks(g, repo):
    hooks = []
    current_hook_dict = {}
    for current_hook in g.get_repo(repo).get_hooks():
        current_hook_dict = {}
        current_hook_dict = {
            "id": current_hook.id,
            "config": current_hook.config,
            "name": current_hook.name,
            "url": current_hook.url,
            "active": current_hook.active,
            "test_url": current_hook.test_url,
            "ping_url": current_hook.ping_url,
            "events": current_hook.events,
        }
        hooks.append(current_hook_dict)
    output = [i for n, i in enumerate(hooks) if i not in hooks[n + 1:]]

    return output


def create_webhook(g, repo, events, url, content_type):

    config = {"url": url, "content_type": content_type if content_type else "json"}

    for current_hook in g.get_repo(repo).get_hooks():
        if (config["url"] == current_hook.config["url"]):
            current_hook.edit("web", config, events, active=True)
            return

    repo = g.get_repo(repo)
    repo.create_hook("web", config, events, active=True)


def delete_webhook(g, repo, url):
    for current_hook in g.get_repo(repo).get_hooks():
        if url == current_hook.config["url"]:
            current_hook.delete()


def run_module():
    module_args = dict(
        state=dict(type="str", default="present"),
        token=dict(type="str", default="No Token Provided."),
        organization_name=dict(type="str", default=""),
        enterprise_url=dict(type="str", default=""),
        repo=dict(type="str", default="No Repo Provided."),
        url=dict(type="str", default=""),
        events=dict(type="list", elements="str"),
        content_type=dict(type="str", default="json"),
    )

    valid_content_types = ["json", "form"]
    valid_actions = ["absent", "present"]
    valid_events = [
        "branch_protection_rule",
        "check_run",
        "check_suite",
        "code_scanning_alert",
        "commit_comment",
        "content_reference",
        "create",
        "delete",
        "deploy_key",
        "deployment",
        "deployment_status",
        "discussion",
        "discussion_comment",
        "fork",
        "github_app_authorization",
        "gollum",
        "installation",
        "installation_repositories",
        "issue_comment",
        "issues",
        "label",
        "marketplace_purchase",
        "member",
        "membership",
        "meta",
        "milestone",
        "organization",
        "org_block",
        "package",
        "page_build",
        "ping",
        "project_card",
        "project_column",
        "project",
        "public",
        "pull_request",
        "pull_request_review",
        "pull_request_review_comment",
        "push",
        "release",
        "repository_dispatch",
        "repository",
        "repository_import",
        "repository_vulnerability_alert",
        "secret_scanning_alert",
        "security_advisory",
        "sponsorship",
        "star",
        "status",
        "team",
        "team_add",
        "watch",
        "workflow_dispatch",
        "workflow_job",
    ]

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.params["state"] not in valid_actions:
        error_message = "Invalid action: " + module.params["state"]
        module.exit_json(changed=False, err=error_message, failed=True)

    if module.params["enterprise_url"] == "":
        g = Github(module.params["token"])
    else:
        g = Github(module.params["token"],
                   base_url=module.params["enterprise_url"])

    if len(module.params["repo"]):
        module.params["repo"] = (
            module.params["organization_name"] + "/" + module.params["repo"]
        )

    initial = get_webhooks(g, module.params["repo"])

    if module.params["url"]:
        if module.params["events"]:
            for event in module.params["events"]:
                if event not in valid_events:
                    error_message = "Invalid event name: " + event
                    module.exit_json(
                        changed=False, err=error_message, failed=True)

        if module.params["state"].lower() == "absent":
            delete_webhook(g, module.params["repo"], module.params["url"])
        elif module.params["state"].lower() == "present":
            if module.params["content_type"] not in valid_content_types:
                error_message = "Invalid content type: " + \
                    module.params["content_type"]
                module.exit_json(changed=False, err=error_message, failed=True)
            create_webhook(
                g,
                module.params["repo"],
                module.params["events"],
                module.params["url"],
                module.params["content_type"],
            )

    output = get_webhooks(g, module.params["repo"])

    result = dict(changed=initial != output, fact="")

    if module.check_mode:
        return result

    module.exit_json(webhooks=output, changed=initial != output)


def main():
    run_module()


if __name__ == "__main__":
    main()
