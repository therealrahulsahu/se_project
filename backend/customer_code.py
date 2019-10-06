def run_main(curr_wid, MW):
    from .customer_order_now import run_main_order_now
    from .customer_status import run_main_status
    from .customer_bill import run_main_bill
    run_main_order_now(curr_wid, MW)
    run_main_status(curr_wid, MW)
    run_main_bill(curr_wid, MW)
