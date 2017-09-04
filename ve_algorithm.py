"""
Module for building a graphical model of a bayesian belief network
and executing the Variable Elimination algorithm upon.
"""


import factor as factor_module
from factor import Factor


class VElimination(object):
    """
    Execute the Variable Elimination algorithm on a graphical model
    containing variables whose values can be observed and factors.
    """
    def __init__(self, variables, factors, query, obs=None):
        """
        Initialize the model.
        :param variables: Variables of the model
        :param factors: Factors of the model
        :param query: Variable to find the conditional probabilities for
        :param obs: observations on the variables of the model
        """
        self.variables = variables
        self.factors = factors
        if obs is None:
            obs = {}
        self.obs = obs
        self.query = query

    def execute(self):
        """
        Variable Elimination Algorithm according to Mackworth & Poole.
        :return: Dict of conditional probabilities of the query variable
        """
        factors = self.factors
        variables = list(self.variables)
        variables.remove(self.query)

        for fac in factors:
            self.set_observations(fac)

        for var in variables:
            if var not in self.obs:
                factors = self.eliminate_variable(var, factors)

        result = factor_module.multiply_batch(self.query, factors)
        denominator = sum(result.get_cpt())
        print(denominator)
        return {val: pr / denominator for val, pr in zip([True, False], result.get_cpt())}

    def set_observations(self, factor):
        """
        Find relevant observed variables for a factor and project the factor
        onto the remaining variables.
        :param factor: Factor object
        """
        relevant_obs = set(self.obs).intersection(set(factor.get_variables()))
        if relevant_obs:
            factor.set_observations({x:self.obs[x] for x in relevant_obs})

    @staticmethod
    def eliminate_variable(variable, factors):
        """
        Eliminate Variable from list of factors by multiplying factors
        containing it and summing the variable out.
        :param variable: Variable to eliminate
        :param factors: list of factors
        :return: list of factors not containing Variable v.
        """
        containing_var = []
        not_containing_var = []
        for fac in factors:
            if variable in fac.get_variables():
                containing_var.append(fac)
            else:
                not_containing_var.append(fac)

        if not containing_var:
            return factors
        else:
            T = factor_module.multiply_batch(variable, containing_var)
            new_factor = factor_module.sum_out(variable, T)
            not_containing_var.append(new_factor)
            return not_containing_var

