class RunMain:
    def __init__(self, curr_wid, MW):
        from backend.chef import RunMainChangeFoodAva, RunMainChefPreparation
        code_change = RunMainChangeFoodAva(curr_wid, MW)
        code_chef_preparation = RunMainChefPreparation(curr_wid, MW)
