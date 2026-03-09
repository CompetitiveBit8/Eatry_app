from models.model_user import UserTable
from schemes.schema import UserDetails
from sqlalchemy import select
from functions import update_details, show_dishes, show_pending_orders, fund_account, show_dishes

def handle_services(option):

    match option:
        case 1:
            update_details()
        case 2:
            show_dishes()
        case 3:
            show_pending_orders()
        case 4:
            fund_account()
        case _:
            show_dishes()