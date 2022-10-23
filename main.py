from pulp import makeDict, lpSum, LpInteger, LpVariable, LpStatusOptimal

import solver

INPUT_PROJECTS = [
    "Project_1",
    "Project_2",
]

INPUT_STUDENTS = [
    "Student_1",
    "Student_2",
    "Student_3",
    "Student_4",
    "Student_5",
    "Student_6",
    "Student_7",
]

INPUT_PRIORITIES = [
    [1, 2], # Student 1
    [2, 1], # Student 2
    [1, 2], # Student 3
    [2, 1], # Student 4
    [1, 2], # Student 5
    [2, 1], # Student 6
    [1, 2], # Student 7
    # Project 1, Project 2
]

possible_assignments = [(s, p) for s in INPUT_STUDENTS for p in INPUT_PROJECTS]

def main():
    priorities = makeDict([INPUT_STUDENTS,INPUT_PROJECTS], INPUT_PRIORITIES, 0)
    assignments = LpVariable.dicts("assign", possible_assignments, 0, 1, LpInteger)
    # go through all the possible assignments and if they are set, we add the priority to the objective function
    # since assignments contains the decision binary variables, the priority is only added, if the student
    # is assigned to the project
    objective = lpSum([assignments[(s, p)] * priorities[s][p] for (s, p) in possible_assignments])
    constraints = []
    # make sure that each student is assigned to exactly one project
    for s in INPUT_STUDENTS:
        constraints.append(lpSum([assignments[(s, p)] for p in INPUT_PROJECTS]) == 1)
    # make sure that each project contains at most 4 students but at least 3
    for p in INPUT_PROJECTS:
        constraints.append(lpSum([assignments[(s, p)] for s in INPUT_STUDENTS]) <= 4)
        # for the final solution this needs to be adjusted since it is totally fine to compleatly ignore a project
        # if there are not enough students. This should be implemented using an additional set of decision variables
        constraints.append(lpSum([assignments[(s, p)] for s in INPUT_STUDENTS]) >= 3)
    # since we strictly set the bounds, we need to ensure that the problem is solvable for all given inputs by running
    # some precondition checks. If the problem is not solvable, we can abort the execution.
    print([c for c in constraints])
    model = solver.construct_gap(solver.create_model("Project_Assignment", solver.LpMaximize), constraints, objective)
    status = model.solve()
    if not status == LpStatusOptimal:
        print("No solution found")
        return
    print(model)
    final_assignments = solver.get_final_assignments(model, INPUT_PROJECTS)
    print("-" * 10)
    print("Solution:")
    for project in final_assignments:
        print(f"{project}: {', '.join(final_assignments[project])}")


if __name__ == '__main__':
    main()

