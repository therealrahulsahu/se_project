class RunMain:
    def __init__(self, curr_wid, MW):
        from .manager_add_food import RunMainAddFood
        code_add_food = RunMainAddFood(curr_wid, MW)

        from .manager_manage_chef import RunMainManageChef
        code_manage_chef = RunMainManageChef(curr_wid, MW)

        from .manager_on_order import RunMainOnOrder
        code_on_order = RunMainOnOrder(curr_wid, MW)

        from .manager_history import RunMainHistory
        code_history = RunMainHistory(curr_wid, MW)

        from .manager_restau import RunMainRestaurant
        code_restaurant = RunMainRestaurant(curr_wid, MW)
