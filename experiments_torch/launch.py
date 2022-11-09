# Copyright 2022 DeepMind Technologies Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Entrypoint for the PyTorch experiments."""

from collections.abc import Sequence

from absl import app
from absl import flags
from experiments_torch import experiment
from ml_collections import config_flags

_CONFIG = config_flags.DEFINE_config_file(
    'config', None, 'Configuration File', lock_config=False)
_DEVICE_ID = flags.DEFINE_integer('device', -1, 'Device ID, -1 for cpu')


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError('Too many command-line arguments.')

  config = _CONFIG.value
  device_id = _DEVICE_ID.value
  experiment.run_program(config.experiment, device_id)


if __name__ == '__main__':
  app.run(main)
