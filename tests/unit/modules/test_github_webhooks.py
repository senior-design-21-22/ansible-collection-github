from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils import basic
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import jsonify
from ansible.module_utils._text import to_bytes
import json
import collections
import unittest


def set_module_args(args):
    if '_ansible_remote_tmp' not in args:
        args['_ansible_remote_tmp'] = '/tmp'
    if '_ansible_keep_remote_files' not in args:
        args['_ansible_keep_remote_files'] = False

    args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
    basic._ANSIBLE_ARGS = to_bytes(args)


class AnsibleExitJson(Exception):
    pass


class AnsibleFailJson(Exception):
    pass


def exit_json(*args, **kwargs):
    if 'changed' not in kwargs:
        kwargs['changed'] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    kwargs['failed'] = True
    raise AnsibleFailJson(kwargs)


def get_webhooks(g, repo):
    webhook_list = []
    if repo == 'test':
        webhook_list = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
    return webhook_list


def create_webhook(g, repo, events, host, endpoint, content_type):

    webhook_list = get_webhooks(g, repo)

    config = {
        "url": "http://%s/%s" % (host, endpoint),
        "content_type": content_type
    }

    for current_hook in webhook_list:
        if(config["url"] == current_hook['config']["url"] and
            current_hook['config']["content_type"] == content_type):
                return webhook_list

    webhook_list.append({
        "id": 67890,
        "config": {
            'url' : config['url'],
            'content_type' : config['content_type']
        },
        "name": 'web',
        "url": 'test_url',
        "active": 'test_active',
        "test_url": 'test_test_url',
        "ping_url": 'test_ping_url',
        "events": events
        })
    return webhook_list


def delete_webhook(g, repo, events, host, endpoint, content_type):
    url = "http://" + host + "/" + endpoint

    webhook_list = get_webhooks(g, repo)

    for current_hook in webhook_list:
        if(collections.Counter(current_hook['events']) == collections.Counter(events) and
           url == current_hook['config']["url"] and
           current_hook['config']["content_type"] == content_type):
            webhook_list.remove(current_hook)

    return webhook_list

def edit_webhook(g, repo, events, host, endpoint, content_type, active_status, add_events, remove_events, new_host, new_endpoint, new_content_type):
    url = "http://" + host + "/" + endpoint
    if new_host:
        host = new_host
    if new_endpoint:
        endpoint = new_endpoint
    config = {
        "url": "http://%s/%s" % (host, endpoint),
        "content_type": content_type
    }

    webhook_list = get_webhooks(g, repo)

    for current_hook in webhook_list:
        if(collections.Counter(current_hook['events']) == collections.Counter(events) and
           url == current_hook['config']["url"] and
           current_hook['config']["content_type"] == content_type):
            if new_host:
                host = new_host
            if new_endpoint:
                endpoint = new_endpoint
            if new_content_type:
                content_type = new_content_type
            new_config = {
                "url": "http://%s/%s" % (host, endpoint),
                "content_type": content_type
            }
            if new_host or new_endpoint or new_content_type:
                current_hook['config'] = new_config
            if active_status.lower() == "false":
                current_hook['config'] = new_config
                current_hook['active'] = 'False'
            if active_status.lower() == "true":
                current_hook['config'] = new_config
                current_hook['active'] = 'True'
            if add_events:
                current_hook['config'] = new_config
                for event in add_events:
                    if event not in current_hook['events']:
                        current_hook['events'].append(event)
            if remove_events:
                current_hook['config'] = new_config
                for event in remove_events:
                    for hook_events in current_hook['events']:
                        if event == hook_events:
                            current_hook['events'].remove(event)

    return webhook_list


def run_module():
    module_args = dict(
        action=dict(type='str', default='add'),
        token=dict(type='str', default='No Token Provided.'),
        organization_name=dict(
            type='str', default=''),
        enterprise_url=dict(type='str', default=''),
        repo=dict(type='str', default='No Repo Provided.'),
        host=dict(type='str', default=''),
        endpoint=dict(type='str', default=''),
        events=dict(type='list', elements='str'),
        content_type=dict(type='str', default=''),
        change_events=dict(type='list', elements='str'),
        active_status=dict(type='str', default=''),
        add_events=dict(type='list', elements='str'),
        remove_events=dict(type='list', elements='str'),
        new_host=dict(type='str', default=''),
        new_endpoint=dict(type='str', default=''),
        new_content_type=dict(type='str', default='')
    )

    valid_content_types = ["json", "form"]
    valid_actions = ["add", "delete", "edit"]
    valid_events = ["branch_protection_rule",
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
                    "workflow_job"]

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    changed = False

    g = 'Github Token'

    result = None
    initial = None

    if module.params['action'] not in valid_actions:
        error_message = 'Invalid action: ' + module.params['action']
        return error_message, changed

    if module.params['repo']:
        initial = get_webhooks(g, module.params['repo'])
        result = initial

    if len(module.params['host']) and len(module.params['endpoint']):
        for event in module.params['events']:
            if event not in valid_events:
                error_message = 'Invalid event name: ' + event
                return error_message, changed
                # module.exit_json(changed=False, err=error_message, failed=True)
        if module.params['add_events']:
            for event in module.params['add_events']:
                if event not in valid_events:
                    error_message = 'Invalid event name: ' + event
                    return error_message, changed
                    # module.exit_json(changed=False, err=error_message, failed=True)
        if module.params['remove_events']:
            for event in module.params['remove_events']:
                if event not in valid_events:
                    error_message = 'Invalid event name: ' + event
                    return error_message, changed
        #             # module.exit_json(changed=False, err=error_message, failed=True)

        if module.params['action'].lower() == 'add':
            if module.params['content_type'] in valid_content_types:
                result = create_webhook(g, module.params['repo'],
                               module.params['events'],
                               module.params['host'],
                               module.params['endpoint'],
                               module.params['content_type'])
        elif module.params['action'].lower() == 'delete':
                result = delete_webhook(g, module.params['repo'],
                               module.params['events'],
                               module.params['host'],
                               module.params['endpoint'],
                               module.params['content_type'])
        elif module.params['action'].lower() == 'edit':
                result = edit_webhook(g, module.params['repo'],
                             module.params['events'],
                             module.params['host'],
                             module.params['endpoint'],
                             module.params['content_type'],
                             module.params['active_status'],
                             module.params['add_events'],
                             module.params['remove_events'],
                             module.params['new_host'],
                             module.params['new_endpoint'],
                             module.params['new_content_type'])


    if initial != result:
        changed = True


    return result, changed

class TestWebhooksModule(unittest.TestCase):
    def test_receive_repository_and_get_webhooks(self):
        set_module_args({
            'repo' : 'test'
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == False


    def test_receive_repository_and_get_no_webhooks(self):
        set_module_args({
            'repo' : 'test_empty'
            })
        result, changed = run_module()
        test = []
        assert result == test
        assert changed == False


    def test_adding_webhook_to_populated_list(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'add',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test_host',
            'endpoint' : 'test_endpoint',
            'content_type' : 'json'
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            },
            {
            "id": 67890,
            "config": {
                'url' : "http://test_host/test_endpoint",
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == True


    def test_adding_webhook_to_empty_list(self):
        set_module_args({
            'repo' : 'test_empty',
            'action' : 'add',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test_host',
            'endpoint' : 'test_endpoint',
            'content_type' : 'json'
            })
        result, changed = run_module()
        test = [{
            "id": 67890,
            "config": {
                'url' : "http://test_host/test_endpoint",
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == True


    def test_adding_webhook_that_is_already_there(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'add',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json'
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == False


    def test_deleting_webhook_from_a_list(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'delete',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json'
            })
        result, changed = run_module()
        test = []
        assert result == test
        assert changed == True


    def test_deleting_webhook_that_is_not_in_a_list(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'delete',
            'events' : ['check_suite'],
            'host' : 'test2.com',
            'endpoint' : 'endpoint2',
            'content_type' : 'json'
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == False

    def test_editing_webhook_that_is_in_a_list_by_changing_configuration(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'new_host' : 'test2.com',
            'new_endpoint' : 'endpoint2'
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test2.com/endpoint2',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == True


    def test_editing_webhook_that_is_in_a_list_by_changing_configuration_and_active_status(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'new_host' : 'test2.com',
            'new_endpoint' : 'endpoint2',
            'active_status' : 'False'
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test2.com/endpoint2',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'False',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == True


    def test_editing_webhook_that_is_in_a_list_by_adding_events(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'add_events' : ['push', 'pull_request']
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite', 'push', 'pull_request']
            }]
        assert result == test
        assert changed == True


    def test_editing_webhook_that_is_in_a_list_by_adding_events_that_are_already_there(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'add_events' : ['check_run', 'check_suite']
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == False


    def test_editing_webhook_that_is_not_in_a_list_by_adding_events(self):
        set_module_args({
            'repo' : 'test_empty',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'add_events' : ['check_run', 'check_suite']
            })
        result, changed = run_module()
        test = []
        assert result == test
        assert changed == False


    def test_editing_webhook_that_is_in_a_list_by_deleting_events(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'remove_events' : ['check_suite']
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run']
            }]
        assert result == test
        assert changed == True


    def test_editing_webhook_that_is_in_a_list_by_deleting_events_that_are_not_there(self):
        set_module_args({
            'repo' : 'test',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'remove_events' : ['pull_request']
            })
        result, changed = run_module()
        test = [{
            "id": 12345,
            "config": {
                'url' : 'http://test.com/endpoint',
                'content_type' : 'json'
            },
            "name": 'web',
            "url": 'test_url',
            "active": 'test_active',
            "test_url": 'test_test_url',
            "ping_url": 'test_ping_url',
            "events": ['check_run', 'check_suite']
            }]
        assert result == test
        assert changed == False


    def test_editing_webhook_that_is_not_in_a_list_by_deleting_events(self):
        set_module_args({
            'repo' : 'test_empty',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'remove_events' : ['pull_request']
            })
        result, changed = run_module()
        test = []
        assert result == test
        assert changed == False


    def test_incorrect_events(self):
        set_module_args({
            'repo' : 'test_empty',
            'action' : 'edit',
            'events' : ['not_an_event', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json'
            })
        result, changed = run_module()
        test = 'Invalid event name: ' + 'not_an_event' 
        assert result == test
        assert changed == False


    def test_incorrect_add_events(self):
        set_module_args({
            'repo' : 'test_empty',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'add_events' : ['not_an_event']
            })
        result, changed = run_module()
        test = 'Invalid event name: ' + 'not_an_event' 
        assert result == test
        assert changed == False


    def test_incorrect_remove_events(self):
        set_module_args({
            'repo' : 'test_empty',
            'action' : 'edit',
            'events' : ['check_run', 'check_suite'],
            'host' : 'test.com',
            'endpoint' : 'endpoint',
            'content_type' : 'json',
            'remove_events' : ['not_an_event']
            })
        result, changed = run_module()
        test = 'Invalid event name: ' + 'not_an_event' 
        assert result == test
        assert changed == False
