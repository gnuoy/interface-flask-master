#!/usr/bin/python
#
# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class FlaskMasterRequires(RelationBase):
    scope = scopes.UNIT

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.

    @hook('{requires:flask-master}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{requires:flask-master}-relation-changed')
    def changed(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')
        if self.data_complete():
            conv.set_state('{relation_name}.available')

    @hook('{requires:flask-master}-relation-{broken,departed}')
    def departed_or_broken(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        if not self.data_complete():
            conv.remove_state('{relation_name}.available')

    def data_complete(self):
        """Check if all information for a Flask Slave connection has been sent

        @returns boolean: True if all required data for connection is present
        """
        if self.master_data and all(self.master_data.values()):
            return True
        return False

    @property
    def master_data(self):
        """Get Flask information from Master

        @returns dict: Return dict of Flask Master info
        """
        for conv in self.conversations():
            data = {
                'message': conv.get_remote('message'),
            }
            if all(data.values()):
                return data
        return {}

    @property
    def message(self):
        """Get message from Master

        @returns str: Return master motd
        """
        return self.master_data.get('message')
