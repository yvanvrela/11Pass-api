from operator import and_
from typing import List
from sqlalchemy import or_, and_, select
from sqlalchemy.orm import Session
from src.infra.database.models.vault_model import VaultModel
from src.infra.schemas import vault_schema


class VaultRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_vault(self, vault: vault_schema.VaultBase) -> VaultModel:
        vault_bd = VaultModel(
            name=vault.name,
            description=vault.description,
            icon_type=vault.icon_type,
            user_id=vault.user_id,
        )
        self.session.add(vault_bd)
        self.session.commit()
        self.session.refresh(vault_bd)
        return vault_bd

    def get_vaults(self, user_id: int) -> List[vault_schema.VaultOut]:
        statement = select(VaultModel).filter_by(user_id=user_id)
        return self.session.execute(statement).scalars().all()

    def get_vault_by_id(self,  vault_id: str, user_id: int) -> VaultModel:
        return self.session.query(VaultModel).filter(
            and_(
                VaultModel.id == vault_id,
                VaultModel.user_id == user_id
            )
        ).first()

    def get_vault_by_name(self,  vault_name: str, user_id: int) -> VaultModel:
        return self.session.query(VaultModel).filter(
            and_(
                VaultModel.name == vault_name,
                VaultModel.user_id == user_id
            )
        ).first()
