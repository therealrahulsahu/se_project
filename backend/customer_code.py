class RunMain:
    def __init__(self, curr_wid, MW):
        from .customer_order_now import RunMainOrderNow
        from .customer_status import RunMainStatus
        from .customer_bill import RunMainBill
        code_order_now = RunMainOrderNow(curr_wid, MW)
        code_status = RunMainStatus(curr_wid, MW)
        code_bill = RunMainBill(curr_wid, MW)
