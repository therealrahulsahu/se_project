class RunMain:
    def __init__(self, curr_wid, MW):
        from backend.customer import RunMainOrderNow, RunMainStatus, RunMainBill
        code_order_now = RunMainOrderNow(curr_wid, MW)
        code_status = RunMainStatus(curr_wid, MW)
        code_bill = RunMainBill(curr_wid, MW)
