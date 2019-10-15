def run_main(curr_wid, MW):
    from .manager_add_food import run_main_add_food
    run_main_add_food(curr_wid, MW)

    from .manager_manage_chef import run_main_manage_chef
    run_main_manage_chef(curr_wid, MW)

    from .manager_on_order import run_main_on_order
    run_main_on_order(curr_wid, MW)

    from .manager_history import run_main_history
    run_main_history(curr_wid, MW)
