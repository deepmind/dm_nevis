"""Functions for loading pretrained models from a checkpoint."""

from typing import Tuple

from absl import logging
import chex
from experiments_jax.training import trainer
import haiku as hk


def load_model_params_from_ckpt(
    params: hk.Params,
    state: hk.State,
    freeze_pretrained_backbone: bool = False,
    checkpoint_path: str = '',
) -> Tuple[hk.Params, hk.Params, hk.State]:
  """Load pretrained model parameter from a checkpoint.

  Args:
    params: original params including trainable heads.
    state: original states.
    freeze_pretrained_backbone: whether to freeze pretrained backbone or not.
    checkpoint_path: path to the pretrained checkpointer.

  Returns:
    updated params split into trainable and frozen, updated states.
  """

  trainer_state = trainer.restore_train_state(checkpoint_path)
  if trainer_state is None or trainer_state.trainable_params is None or trainer_state.frozen_params is None:
    return params, {}, state

  restored_params = {
      **trainer_state.trainable_params,
      **trainer_state.frozen_params
  }

  def filter_fn(module_name, *unused_args):
    del unused_args
    return module_name.startswith('backbone')

  filtered_original_params = hk.data_structures.filter(filter_fn, params)
  filtered_params = hk.data_structures.filter(filter_fn, restored_params)

  chex.assert_trees_all_equal_shapes(filtered_original_params, filtered_params)

  # replace the initialized params by pretrained params
  updated_params = hk.data_structures.merge(params, filtered_params)

  if freeze_pretrained_backbone:
    frozen_params, trainable_params = hk.data_structures.partition(
        filter_fn, updated_params)
  else:
    trainable_params = updated_params
    frozen_params = {}

  logging.info('Loading pretrained model finished.')

  return trainable_params, frozen_params, state
