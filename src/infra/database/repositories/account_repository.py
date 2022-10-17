from typing import List
from sqlalchemy import or_, and_, select
from sqlalchemy.orm import Session
from src.infra.database.models.user_model import UserModel
from src.infra.database.models.account_model import AccountModel
from src.infra.schemas import account_schema


class AccountRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_account(self, account:account_schema.AccountBase)-> AccountModel:
        account_db = AccountModel(
            name=account.name,
            username=account.username,
            email=account.email,
            password=account.password,
            description=account.description,
            page_url=account.page_url,
            vault_id=account.vault_id,
            user_id = account.user_id,
        )
        self.session.add(account_db)
        self.session.add
        return account_db

    def get_account_by_name(self,  account_name: str, user_id: int) -> AccountModel:
        return self.session.query(AccountModel).filter(
            and_(
                AccountModel.name == account_name,
                AccountModel.user_id == user_id
            )
        ).first()