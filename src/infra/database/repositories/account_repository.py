from typing import List
from sqlalchemy import or_, and_, select
from sqlalchemy.orm import Session
from src.infra.database.models.user_model import UserModel
from src.infra.database.models.account_model import AccountModel
from src.infra.schemas import account_schema


class AccountRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_account(self, account: account_schema.AccountCreate) -> AccountModel:
        account_db = AccountModel(
            name=account.name,
            username=account.username,
            email=account.email,
            password=account.password,
            description=account.description,
            icon_type=account.icon_type,
            page_url=account.page_url,
            vault_id=account.vault_id,
            user_id=account.user_id,
        )
        self.session.add(account_db)
        self.session.commit()
        self.session.refresh(account_db)
        return account_db

    def get_accounts(self, user_id: int) -> List[account_schema.AccountCreate]:
        statement = select(AccountModel).join_from(
            AccountModel, UserModel).where(AccountModel.user_id == user_id)
        return self.session.execute(statement).scalars().all()

    def get_account_by_name(self,  account_name: str, user_id: int) -> AccountModel:
        return self.session.query(AccountModel).filter(
            and_(
                AccountModel.name == account_name,
                AccountModel.user_id == user_id
            )
        ).first()

    def get_account_by_id(self, account_id: int, user_id: int) -> AccountModel:
        return self.session.query(AccountModel).filter(
            and_(
                AccountModel.id == account_id,
                AccountModel.user_id == user_id
            )
        ).first()

    def update_account(self, user_id: int, account_id: id, update_data: account_schema.AccountCreate) -> AccountModel:
        account_db = self.get_account_by_id(account_id, user_id)

        account_db.name = update_data.name
        account_db.username = update_data.username
        account_db.email = update_data.email
        account_db.password = update_data.password
        account_db.description = update_data.description
        account_db.page_url = update_data.page_url
        account_db.icon_type = update_data.icon_type

        self.session.add(account_db)
        self.session.commit()
        self.session.refresh(account_db)
        return account_db

    def delete_account(self, account_id: int, user_id: int) -> AccountModel:
        account_db = self.get_account_by_id(account_id, user_id)

        self.session.delete(account_db)
        self.session.commit()
        return account_db
