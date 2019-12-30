def run_main(curr_wid, MW):
    from backend.customer import RunMainOrderNow, RunMainStatus, RunMainBill
    RunMainOrderNow(curr_wid, MW)
    RunMainStatus(curr_wid, MW)
    RunMainBill(curr_wid, MW)
