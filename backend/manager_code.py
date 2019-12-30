def run_main(curr_wid, MW):
    from backend.manager import RunMainAddFood, RunMainManageChef, \
        RunMainOnOrder, RunMainHistory, RunMainRestaurant
    RunMainAddFood(curr_wid, MW)
    RunMainManageChef(curr_wid, MW)
    RunMainOnOrder(curr_wid, MW)
    RunMainHistory(curr_wid, MW)
    RunMainRestaurant(curr_wid, MW)
