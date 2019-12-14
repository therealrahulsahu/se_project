class RunMain:
    def __init__(self, curr_wid, MW):
        from backend.manager import RunMainAddFood, RunMainManageChef, \
            RunMainOnOrder, RunMainHistory, RunMainRestaurant
        code_add_food = RunMainAddFood(curr_wid, MW)
        code_manage_chef = RunMainManageChef(curr_wid, MW)
        code_on_order = RunMainOnOrder(curr_wid, MW)
        code_history = RunMainHistory(curr_wid, MW)
        code_restaurant = RunMainRestaurant(curr_wid, MW)
