#
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: EPL-2.0
#

import os
from shutil import copytree
from mlt.commands import Command
from mlt.utils import (git_helpers, config_helpers)
from mlt.utils import constants


class UpdateTemplateCommand(Command):
    def __init__(self, args):
        super(UpdateTemplateCommand, self).__init__(args)
        self.config = config_helpers.load_config()
        self.template_repo = self.args["--template-repo"]

    def action(self):
        """Update the template instance with new template version
         if template is updated """
        current_template_git_sha = self.config["template_git_sha"]
        orig_project_backup_dir = os.path.join(os.getcwd(),
                                               os.pardir,
                                               self.config["name"] + ".orig")

        with git_helpers.clone_repo(self.template_repo) as temp_clone:
            template_folder = os.path.join(constants.TEMPLATES_DIR,
                                           self.config["template_name"])
            latest_template_git_sha = git_helpers. \
                get_latest_sha(temp_clone, template_folder)
            if current_template_git_sha == latest_template_git_sha:
                print("Template is up to date. No need for update!")
            else:
                print("Template is NOT up to date. Updating template!")
                copytree(os.getcwd(), orig_project_backup_dir)
                # TODO: apply the latest changes, if conflict keep the
                # original folder intact graceful error out.
