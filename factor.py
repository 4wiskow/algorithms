"""
Definition of a Factor class as well as some operations on factors necessary for the
Variable Elimination algorithm (Mackworth&Poole 2010).
"""

import functools


class Factor(object):
    """
    A Factor contains a conditional probability table (cpt) for an arbitrary amount of
    boolean variables. Their values can be observed to reduce the size of the cpt.
    """
    domain = [True, False]

    def __init__(self, variables, probabilities, obs=None):
        """
        Initialize the factor
        :param variables: List of variables in the factor. The last variable is the dependent one
        :param probabilities: the probability distribution of this factor as a list
        :param obs: Dict of Observations about any of the variables in this factor
        """
        if obs is None:
            obs = {}
        self.obs = obs  # {variable:value}
        self.variables = variables
        self.cpt = probabilities

    def set_observations(self, obs):
        """
        Delete rows from the conditional probability table that are contrary to the observations.
        :param obs: Dict of variables and their observed values
        """
        new_cpt = []

        for key in iter(obs.keys()):
            for index in range(len(self.cpt)):
                if int(self.get_bin_value(key, index)) != obs[key]:
                    new_cpt.append(self.cpt[index])
            self.variables.remove(key)

        self.cpt = new_cpt

    def get_cpt(self):
        return self.cpt

    def get_variables(self):
        return list(self.variables)

    def index_of_variable(self, variable):
        return self.variables.index(variable)

    def get_bin_value(self, var, val_ind):
        """
        Get the binary value of the Variable var at integer index val_ind.
        E.g. self.variables = A, B; var = B;
        val_ind= 1 -> binary val_ind = 01, result = 1
        :param var: the variable at whose position to read the binary value
        :param val_ind: the index of the value of the cpt
        :return: binary value; 0 or 1
        """
        index = self.index_of_variable(var)
        number_of_vars = str(len(self.variables))
        bindex = format(val_ind, '0' + number_of_vars + 'b')
        return bindex[index]


def unionize_factors(var, facs):
    """
    Multiply two factors with a common Variable var.
    :param var: common variable
    :param factors: two factors to be multiplied
    :return: table of values of new factor
    """
    results = []

    for first_index, first_val in enumerate(facs[0].get_cpt()):
        bin_value = facs[0].get_bin_value(var, first_index)
        for sec_index, second_val in enumerate(facs[1].get_cpt()):
            corresponding_bin = facs[1].get_bin_value(var, sec_index)
            if bin_value == corresponding_bin:
                new_val = first_val*second_val
                results.append(new_val)

    vars_two = facs[1].get_variables()
    vars_two.remove(var)
    vars_new_factor = facs[0].get_variables() + vars_two
    unionized_factor = Factor(vars_new_factor, results)
    return unionized_factor


def multiply_batch(var, factors):
    """
    unionize multiple factors.
    :param var: common variable
    :param factors: list of factors to unionize
    :return: factor
    """
    facs = [f for f in factors if var in f.get_variables()]
    return functools.reduce(lambda x, y: unionize_factors(var, [x, y]), facs)


def sum_out(var, factor):
    """
    Sum a variable out of a factor.
    :param var: variable to be summed out
    :param factor: factor to sum out of
    :return: new factor with variables reduced by var. CPT size reduced by factor 2.
    """
    values_todo = factor.get_cpt()
    indices_done = []
    index_of_var = factor.index_of_variable(var)
    number_of_vars = len(factor.get_variables())

    results = []
    for index, val in enumerate(values_todo):
        if index not in indices_done:
            bin_index = number_of_vars - index_of_var - 1
            complementary_index = index ^ (1 << bin_index)
            # Complementary value is at original position bin_index
            # with Bit at pos of relevant Variable flipped.
            # e.g. sum out B: ABCD tttt + tftt = ACD ttt
            #                 ABCD 0000 + 0100 = ACD 000
            complementary_val = values_todo[complementary_index]

            results.append(val + complementary_val)
            indices_done.append(index)
            indices_done.append(complementary_index)
    new_vars = factor.get_variables()
    new_vars.remove(var)
    new_factor = Factor(new_vars, results)
    return new_factor
