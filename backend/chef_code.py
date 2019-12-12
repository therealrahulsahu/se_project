class RunMain:
    def __init__(self, curr_wid, MW):
        from .chef_change_food_ava import RunMainChangeFoodAva
        code_change = RunMainChangeFoodAva(curr_wid, MW)

        from .chef_preparation import RunMainChefPreparation
        code_chef_preparation = RunMainChefPreparation(curr_wid, MW)


def run_main(curr_wid, MW):
    from .chef_change_food_ava import run_main_change_food_ava
    run_main_change_food_ava(curr_wid, MW)

    from .chef_preparation import run_main_chef_preparation
    run_main_chef_preparation(curr_wid, MW)
