# Copyright 2020 The Google Earth Engine Community Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections.abc import Sequence
import dataclasses
import itertools
import os
from typing import Optional

from absl import app
from absl import logging
import h5py
import numpy as np
import pandas as pd

import gedi_lib


@dataclasses.dataclass(frozen=True, kw_only=True)
class GediVars:
  integer_variables: Sequence[str] = dataclasses.field(default_factory=list)
  float_variables: Sequence[str] = dataclasses.field(default_factory=list)
  string_variables: Sequence[str] = dataclasses.field(default_factory=list)

  def numeric_vars(self) -> list[str]:
    """Returns all numeric variables sorted alphanumerically."""
    return sorted(itertools.chain(self.integer_variables, self.float_variables))

  def all_vars(self) -> list[str]:
    """Returns all variables sorted alphanumerically."""
    return sorted(itertools.chain(self.numeric_vars(), self.string_variables))


gedi_vars = GediVars(
    integer_variables=(
        'algorithm_run_flag',
        'beam',
        'channel',
        'degrade_flag',
        'l2_quality_flag',
        'l4_quality_flag',
        'master_int',
        'predictor_limit_flag',
        'response_limit_flag',
        'selected_algorithm',
        'selected_mode',
        'selected_mode_flag',
        'surface_flag',
    ),
    float_variables=(
        'agbd',
        'agbd_pi_lower',
        'agbd_pi_upper',
        'agbd_se',
        'agbd_t',
        'agbd_t_se',
        'delta_time',
        'elev_lowestmode',
        'lat_lowestmode',
        'lon_lowestmode',
        'master_frac',
        'sensitivity',
        'solar_elevation',
    ),
    string_variables=(
        'shot_number',
        'predict_stratum',
    ),
)

group_vars = {
    'agbd_prediction': GediVars(
        integer_variables=(
            'algorithm_run_flag_a1',
            'algorithm_run_flag_a10',
            'algorithm_run_flag_a2',
            'algorithm_run_flag_a3',
            'algorithm_run_flag_a4',
            'algorithm_run_flag_a5',
            'algorithm_run_flag_a6',
            'l2_quality_flag_a1',
            'l2_quality_flag_a10',
            'l2_quality_flag_a2',
            'l2_quality_flag_a3',
            'l2_quality_flag_a4',
            'l2_quality_flag_a5',
            'l2_quality_flag_a6',
            'l4_quality_flag_a1',
            'l4_quality_flag_a10',
            'l4_quality_flag_a2',
            'l4_quality_flag_a3',
            'l4_quality_flag_a4',
            'l4_quality_flag_a5',
            'l4_quality_flag_a6',
            'predictor_limit_flag_a1',
            'predictor_limit_flag_a10',
            'predictor_limit_flag_a2',
            'predictor_limit_flag_a3',
            'predictor_limit_flag_a4',
            'predictor_limit_flag_a5',
            'predictor_limit_flag_a6',
            'response_limit_flag_a1',
            'response_limit_flag_a10',
            'response_limit_flag_a2',
            'response_limit_flag_a3',
            'response_limit_flag_a4',
            'response_limit_flag_a5',
            'response_limit_flag_a6',
            'selected_mode_a1',
            'selected_mode_a10',
            'selected_mode_a2',
            'selected_mode_a3',
            'selected_mode_a4',
            'selected_mode_a5',
            'selected_mode_a6',
            'selected_mode_flag_a1',
            'selected_mode_flag_a10',
            'selected_mode_flag_a2',
            'selected_mode_flag_a3',
            'selected_mode_flag_a4',
            'selected_mode_flag_a5',
            'selected_mode_flag_a6',
        ),
        float_variables=(
            'agbd_a1',
            'agbd_a10',
            'agbd_a2',
            'agbd_a3',
            'agbd_a4',
            'agbd_a5',
            'agbd_a6',
            'agbd_pi_lower_a1',
            'agbd_pi_lower_a10',
            'agbd_pi_lower_a2',
            'agbd_pi_lower_a3',
            'agbd_pi_lower_a4',
            'agbd_pi_lower_a5',
            'agbd_pi_lower_a6',
            'agbd_pi_upper_a1',
            'agbd_pi_upper_a10',
            'agbd_pi_upper_a2',
            'agbd_pi_upper_a3',
            'agbd_pi_upper_a4',
            'agbd_pi_upper_a5',
            'agbd_pi_upper_a6',
            'agbd_se_a1',
            'agbd_se_a10',
            'agbd_se_a2',
            'agbd_se_a3',
            'agbd_se_a4',
            'agbd_se_a5',
            'agbd_se_a6',
            'agbd_t_a1',
            'agbd_t_a10',
            'agbd_t_a2',
            'agbd_t_a3',
            'agbd_t_a4',
            'agbd_t_a5',
            'agbd_t_a6',
            'agbd_t_pi_lower_a1',
            'agbd_t_pi_lower_a10',
            'agbd_t_pi_lower_a2',
            'agbd_t_pi_lower_a3',
            'agbd_t_pi_lower_a4',
            'agbd_t_pi_lower_a5',
            'agbd_t_pi_lower_a6',
            'agbd_t_pi_upper_a1',
            'agbd_t_pi_upper_a10',
            'agbd_t_pi_upper_a2',
            'agbd_t_pi_upper_a3',
            'agbd_t_pi_upper_a4',
            'agbd_t_pi_upper_a5',
            'agbd_t_pi_upper_a6',
            'agbd_t_se_a1',
            'agbd_t_se_a10',
            'agbd_t_se_a2',
            'agbd_t_se_a3',
            'agbd_t_se_a4',
            'agbd_t_se_a5',
            'agbd_t_se_a6',
        ),
    ),
    'geolocation': GediVars(
        integer_variables=('stale_return_flag',),
        float_variables=(
            'elev_lowestmode_a1',
            'elev_lowestmode_a10',
            'elev_lowestmode_a2',
            'elev_lowestmode_a3',
            'elev_lowestmode_a4',
            'elev_lowestmode_a5',
            'elev_lowestmode_a6',
            'lat_lowestmode_a1',
            'lat_lowestmode_a10',
            'lat_lowestmode_a2',
            'lat_lowestmode_a3',
            'lat_lowestmode_a4',
            'lat_lowestmode_a5',
            'lat_lowestmode_a6',
            'lon_lowestmode_a1',
            'lon_lowestmode_a10',
            'lon_lowestmode_a2',
            'lon_lowestmode_a3',
            'lon_lowestmode_a4',
            'lon_lowestmode_a5',
            'lon_lowestmode_a6',
            'sensitivity_a1',
            'sensitivity_a10',
            'sensitivity_a2',
            'sensitivity_a3',
            'sensitivity_a4',
            'sensitivity_a5',
            'sensitivity_a6',
        ),
    ),
    'land_cover_data': GediVars(
        integer_variables=(
            'landsat_water_persistence',
            'leaf_off_doy',
            'leaf_off_flag',
            'leaf_on_cycle',
            'leaf_on_doy',
            'pft_class',
            'region_class',
            'urban_focal_window_size',
            'urban_proportion',
        ),
        float_variables=('landsat_treecover',),
    ),
}

filled_vars_float = [
    'agbd', 'agbd_pi_lower', 'agbd_pi_upper', 'agbd_se', 'agbd_t', 'agbd_t_se',
    'agbd_a1', 'agbd_a10', 'agbd_a2', 'agbd_a3', 'agbd_a4', 'agbd_a5',
    'agbd_a6', 'agbd_pi_lower_a1', 'agbd_pi_lower_a10', 'agbd_pi_lower_a2',
    'agbd_pi_lower_a3', 'agbd_pi_lower_a4', 'agbd_pi_lower_a5',
    'agbd_pi_lower_a6', 'agbd_pi_upper_a1', 'agbd_pi_upper_a10',
    'agbd_pi_upper_a2', 'agbd_pi_upper_a3', 'agbd_pi_upper_a4',
    'agbd_pi_upper_a5', 'agbd_pi_upper_a6', 'agbd_se_a1', 'agbd_se_a10',
    'agbd_se_a2', 'agbd_se_a3', 'agbd_se_a4', 'agbd_se_a5', 'agbd_se_a6',
    'agbd_t_a1', 'agbd_t_a10', 'agbd_t_a2', 'agbd_t_a3', 'agbd_t_a4',
    'agbd_t_a5', 'agbd_t_a6', 'agbd_t_pi_lower_a1', 'agbd_t_pi_lower_a10',
    'agbd_t_pi_lower_a2', 'agbd_t_pi_lower_a3', 'agbd_t_pi_lower_a4',
    'agbd_t_pi_lower_a5', 'agbd_t_pi_lower_a6', 'agbd_t_pi_upper_a1',
    'agbd_t_pi_upper_a10', 'agbd_t_pi_upper_a2', 'agbd_t_pi_upper_a3',
    'agbd_t_pi_upper_a4', 'agbd_t_pi_upper_a5', 'agbd_t_pi_upper_a6',
    'agbd_t_se_a1', 'agbd_t_se_a10', 'agbd_t_se_a2', 'agbd_t_se_a3',
    'agbd_t_se_a4', 'agbd_t_se_a5', 'agbd_t_se_a6'
]

filled_vars_byte = [
    'predictor_limit_flag',
    'predictor_limit_flag_a1',
    'predictor_limit_flag_a10',
    'predictor_limit_flag_a2',
    'predictor_limit_flag_a3',
    'predictor_limit_flag_a4',
    'predictor_limit_flag_a5',
    'predictor_limit_flag_a6',
    'response_limit_flag',
    'response_limit_flag_a1',
    'response_limit_flag_a10',
    'response_limit_flag_a2',
    'response_limit_flag_a3',
    'response_limit_flag_a4',
    'response_limit_flag_a5',
    'response_limit_flag_a6'
]


def extract_values(input_paths: Sequence[str], output_path: str) -> None:
  """Extracts all variables from all algorithms.

  Args:
     input_paths: GEDI L4A file paths
     output_path: csv output file path
  """
  assert len(input_paths) == 1
  l4a_path = input_paths[0]
  basename = os.path.basename(l4a_path)
  if not basename.startswith('GEDI') or not basename.endswith('.h5'):
    logging.error('Input path is not a GEDI filename: %s', l4a_path)
    return

  with h5py.File(l4a_path, 'r') as l4a_hdf_fh:
    with open(output_path, 'w') as csv_fh:
      write_csv(l4a_hdf_fh, csv_fh)


def write_csv(l4a_hdf_fh, csv_file):
  """Writes a single CSV file based on the contents of HDF file."""
  is_first = True
  # Iterating over relative height percentage values from 0 to 100
  for k in l4a_hdf_fh.keys():
    if not k.startswith('BEAM'):
      continue
    print('\t', k)

    df = pd.DataFrame()

    for v in gedi_vars.all_vars():
      gedi_lib.hdf_to_df(l4a_hdf_fh, k, v, df)

    # Add the incidence angle variables from the corresponding L2B file.
    for group_var, l4a_vars in group_vars.items():
      for l4a_var in l4a_vars.all_vars():
        gedi_lib.hdf_to_df(l4a_hdf_fh, k, f'{group_var}/{l4a_var}', df)
    df[filled_vars_float] = df.loc[:, filled_vars_float].replace(
        to_replace=-9999, value=np.nan)
    df[filled_vars_byte] = df.loc[:, filled_vars_byte].replace(
        to_replace=255, value=np.nan)

    # Filter our rows with nan values for lat_lowestmode or lon_lowestmode.
    # Such rows are not ingestable into EE.
    df = df[df.lat_lowestmode.notnull()]
    df = df[df.lon_lowestmode.notnull()]
    gedi_lib.add_shot_number_breakdown(df)

    df.to_csv(
        csv_file,
        float_format='%3.6f',
        index=False,
        header=is_first,
        mode='a',
        lineterminator='\n',
    )
    is_first = False


def main(argv):
  extract_values([argv[1]], argv[2])

if __name__ == '__main__':
  app.run(main)
