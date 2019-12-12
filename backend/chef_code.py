class RunMain:
    def __init__(self, curr_wid, MW):
        from .chef_change_food_ava import RunMainChangeFoodAva
        code_change = RunMainChangeFoodAva(curr_wid, MW)

        from .chef_preparation import RunMainChefPreparation
        code_chef_preparation = RunMainChefPreparation(curr_wid, MW)
