.. _collaborator_information:


********************
collaborator_information
********************

**This module was created to manage collaborators.**


Version added: 0.0.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Retrieve Github organization collaborator information in the form of a dictionary of repositories each containing a list of dictionaries that contain collaborator information.
- Manage GitHub collaborators in organization repositories including adding, removing, changing permissions, or checking permissions.


Requirements
------------
There are no further requirements needed to run this module.


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
  <!-- TOP OF TABLE -->
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th>Choices/<font color="blue">Required</font></th>
            <th width="50%">Comments</th>
        </tr>
  <!-- GITHUB TOKEN -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>GitHub Token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>True</div>
                </td>
                <td>
                        <div>Token used to authenticate with the Github Rest API.</div>
                </td>
            </tr>
  <!-- ORG_NAME -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>organization_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>True</div>
                </td>
                <td>
                        <div>Organization provided by users.</div>
                </td>
            </tr>
  <!-- ENTERPRISE_URL -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>enterprise_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <div>Unecessary in event of user token</div>
                </td>
                <td>
                        <div>False</div>
                </td>
                <td>
                        <div>Enterprise url is necessary when module is recieving an enterprise token</div>
                </td>
            </tr>
  <!-- REPOSITORIES LIST-->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>repos</b>                                                                            <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div></div>                                                                         <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>True</div>
                </td>
                <td>
                        <div>List of repositories is provided by user to perform further action upon</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- COLLABORATORS TO ADD-->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>collaborators_to_add</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list/dict</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div>Add by providing a list of dicts of collaborators to add along with their permissions or provide a single collaborator with their intended permission</div><!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>
                </td>
                <td>
                        <div>Collaborator(s) are added along with their intended permissions (Read, Triage, Write, Maintain, or Admin) to the provided list of repos</div>  <!-- COMMENTS -->
                </td>
            </tr>
    <!-- COLLABORATORS TO REMOVE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>collaborators_to_remove</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list of string</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div>Delete collaborator(s) by providing a list of collaborator names (string).</div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>This will delete all of the provided collaborators from the repos provided.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
    <!-- CHECK COLLABORATOR -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>check_collaborator</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dict</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div>A name as the Key and a permission to check is provided by the user.</div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>This will check the provided permission against the given repos.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
            
    <!-- COLLABORATORS TO CHANGE -->
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>collaborators_to_change</b>                                                             <!-- PARAMETER -->
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dict</span>                                             <!-- TYPE -->
                    </div>
                </td>
                <td>
                        <div>A name as the Key and a permission to check is provided by the user.</div>      <!-- CHOICES/DEFAULTS -->
                </td>
                <td>
                        <div>False</div>                                                                         <!-- REQUIRED -->
                </td>
                <td>
                        <div>This will check the provided permission against the given repos.</div>  <!-- COMMENTS -->
                </td>
            </tr> 
       
            
            
    <!-- END OF TABLE-->      
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: "Listing collaborators from enterprise GitHub account"
      ohioit.github.collaborator_information:
        token: "[token]"
        organization_name: "[org name]"
        enterprise_url: "https://github.com/put/your/url/here"
        repos:
          - "[repo 1]"
          - "[repo 2]"
          - "[repo 3]"
      register: result

    - name: "Adding collaborators from enterprise GitHub account"
      ohioit.github.collaborator_information:
        token: "[token]"
        organization_name: "[org name]"
        enterprise_url: "https://github.com/put/your/url/here"
        repos:
          - "[repo 1]"
          - "[repo 2]"
          - "[repo 3]"
        collaborators_to_add:
          [GitHub Username]: "[triage, pull, push or admin]"
          
      register: result

    - name: "Check permissions of collaborators from enterprise GitHub account"
      ohioit.github.collaborator_information:
        token: "[token]"
        organization_name: "[org name]"
        enterprise_url: "https://github.com/put/your/url/here"
        repos:
          - "[repo 1]"
          - "[repo 2]"
          - "[repo 3]"
        check_collaborator:
          [GitHub Username]: "[triage, pull, push or admin]"

      register: result

    - name: "Change permissions of collaborators from enterprise GitHub account"
      ohioit.github.collaborator_information:
        token: "[token]"
        organization_name: "[org name]"
        enterprise_url: "https://github.com/put/your/url/here"
        repos:
          - "[repo 1]"
          - "[repo 2]"
          - "[repo 3]"
        collaborators_to_change:
          [GitHub Username]: "[triage, pull, push or admin]"
      register: result

    - name: "Remove permissions of collaborators from enterprise GitHub account"
      ohioit.github.collaborator_information:
        token: "[token]"
        organization_name: "[org name]"
        enterprise_url: "https://github.com/put/your/url/here"
        repos:
          - "[repo 1]"
          - "[repo 2]"
          - "[repo 3]"
        collaborators_to_remove:
          - "[GitHub Username]"
      register: result
      
     

Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>                                                                           
            <th width="50%">Description</th>
        </tr>
  <!-- returned value -->
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>Result.msg</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dict</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>Always</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>The List data structure is composed of the dictionaries containing repos along with their names and other useful information.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all; background-color:#958E8D;">
                          <pre style="background-color:#958E8D;"><code style="background-color:#958E8D;">{
    "[repo 1]":
        [
            {
                "login":                owner name as string,
                "id":                   description as int,
                "type":                 user type as string
                "site_admin":           site admin access as boolean,
                "permissions":          user permissions as Permissions dictionary
            },
            {
                ...
            }
        ],
    "[repo 2]":
        [
          ...
        ],
        ...
 }</code></pre>
                        </div>
                </td>
            </tr>
            
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>Result.changed</b>                                                                     <!-- HOW TO ACCESS RETURNED -->
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">bool</span>                                               <!-- TYPE -->
                    </div>
                </td>
                <td>Always</td>                                                                             <!-- WHEN IS IT RETURNED -->
                <td>
                            <div>Whether or not any of the collaborator statuses were changed. Either true (something changed) or false (nothing changed).</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Brad Golski (@bgolski)
- Jacob Eicher (@jacobeicher)
- Nolan Khounborin (@khounborinn)
- Tyler Zwolenik (@TylerZwolenik)
