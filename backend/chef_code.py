def run_main(curr_wid, MW):
    from backend.chef import RunMainChangeFoodAva, RunMainChefPreparation
    RunMainChangeFoodAva(curr_wid, MW)
    RunMainChefPreparation(curr_wid, MW)
