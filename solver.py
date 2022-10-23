from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpAffineExpression


def create_model(name: str, sense: int = LpMaximize) -> LpProblem:
    """
    Create a model with a given name and sense using PulP
    :param name: of the model to be created
    :param sense: of the model to be created
    :return: LpProblem object representing the model
    """
    return LpProblem(name=name, sense=sense)


def construct_gap(model: LpProblem, constraints: list, objective: LpAffineExpression) -> LpProblem:
    """
    Given a problem a set of constraints and an objective function, construct the model
    :param model: to be constructed
    :param constraints: list of constraints to be added to the model
    :param objective: objective function of the model
    :return: LpProblem object representing the model
    """
    for expression in constraints:
        model += expression
    model += objective
    return model


def get_final_assignments(model: LpProblem, projects: list) -> dict:
    """
    Given a model and a list of projects, return a dictionary containing the final assignments
    :param model: to be evaluated
    :param projects: list of projects
    :return: dictionary containing the final assignments
    """
    assignments = {}
    for project in projects:
        assignments[project] = []
        for variable in model.variables():
            if variable.varValue == 1 and project in variable.name:
                assignments[project].append(get_variable_subject(variable.name))
    return assignments


def get_variable_subject(name):
    result = name.split("_")[1].replace("'", "").replace("(", "")
    return result + name.split("_")[2].replace("'", "").replace(",", "")
