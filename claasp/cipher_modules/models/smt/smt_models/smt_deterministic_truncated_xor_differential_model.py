
# ****************************************************************************
# Copyright 2023 Technology Innovation Institute
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ****************************************************************************


from claasp.cipher_modules.models.smt.smt_model import SmtModel
from claasp.name_mappings import CONSTANT, INTERMEDIATE_OUTPUT, CIPHER_OUTPUT, WORD_OPERATION


class SmtXorDifferentialModel(SmtModel):
    def __init__(self, cipher, counter='sequential'):
        super().__init__(cipher, counter)

    def build_deterministic_truncated_xor_differential_trail_model(self, fixed_variables=[]):
        """
        Build the model for the search of deterministic truncated XOR differential trails.

        INPUT:

        - ``fixed_variables`` -- **list** (default: `[]`); the variables to be fixed in standard format

        .. SEEALSO::

            :py:meth:`~cipher_modules.models.utils.set_fixed_variables`

        EXAMPLES::

            sage: from claasp.ciphers.block_ciphers.speck_block_cipher import SpeckBlockCipher
            sage: from claasp.cipher_modules.models.smt.smt_models.smt_deterministic_truncated_xor_differential_model import SmtXorDifferentialModel
            sage: speck = SpeckBlockCipher(number_of_rounds=22)
            sage: smt = SmtXorDifferentialModel(speck)
            sage: smt.build_deterministic_truncated_xor_differential_trail_model()
            ...
        """
        variables = []
        constraints = self.fix_variables_value_constraints(fixed_variables)
        self._variables_list = []
        self._model_constraints = constraints

        for component in self._cipher.get_all_components():
            component_types = [CONSTANT, INTERMEDIATE_OUTPUT, CIPHER_OUTPUT, WORD_OPERATION]
            operation = component.description[0]
            operation_types = ["ROTATE", "SHIFT"]

            if component.type in component_types and (component.type != WORD_OPERATION or operation in operation_types):
                variables, constraints = component.smt_deterministic_truncated_xor_differential_trail_constraints()
            else:
                print(f'{component.id} not yet implemented')

            self._variables_list.extend(variables)
            self._model_constraints.extend(constraints)
