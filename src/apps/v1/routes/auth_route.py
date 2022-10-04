from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from src.infra.schemas import user_schema
from src.infra.database.repositories.user_repository import UserRepository
from src.infra.database.config.database import get_db
from src.core import security
from src.infra.providers import password_provider


router = APIRouter()


