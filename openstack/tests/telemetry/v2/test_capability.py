# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import mock
import testtools

from openstack.telemetry.v2 import capability

EXAMPLE = {
    "id": "123",
    "enabled": False,
}
BODY = {
    "api": {
        "statistics:query:complex": False,
        "alarms:history:query:simple": True,
        "events:query:simple": True,
        "alarms:query:simple": True,
        "resources:query:simple": True,
    }
}


class TestCapability(testtools.TestCase):
    def test_basic(self):
        sot = capability.Capability()
        self.assertEqual('capability', sot.resource_key)
        self.assertEqual('capabilities', sot.resources_key)
        self.assertEqual('/v2/capabilities', sot.base_path)
        self.assertEqual('metering', sot.service.service_type)
        self.assertFalse(sot.allow_create)
        self.assertFalse(sot.allow_retrieve)
        self.assertFalse(sot.allow_update)
        self.assertFalse(sot.allow_delete)
        self.assertTrue(sot.allow_list)

    def test_make_it(self):
        sot = capability.Capability(EXAMPLE)
        self.assertEqual(EXAMPLE['id'], sot.id)
        self.assertEqual(EXAMPLE['enabled'], sot.enabled)

    def test_list(self):
        sess = mock.Mock()
        resp = mock.Mock()
        resp.body = BODY
        sess.get = mock.Mock(return_value=resp)

        caps = capability.Capability.list(sess)

        caps = sorted(caps, key=lambda cap: cap.id)
        self.assertEqual(5, len(caps))
        self.assertEqual('alarms:history:query:simple', caps[0].id)
        self.assertEqual(True, caps[0].enabled)
        self.assertEqual('alarms:query:simple', caps[1].id)
        self.assertEqual(True, caps[1].enabled)
        self.assertEqual('events:query:simple', caps[2].id)
        self.assertEqual(True, caps[2].enabled)
        self.assertEqual('resources:query:simple', caps[3].id)
        self.assertEqual(True, caps[3].enabled)
        self.assertEqual('statistics:query:complex', caps[4].id)
        self.assertEqual(False, caps[4].enabled)
