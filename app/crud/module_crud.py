from sqlalchemy.orm import Session

from app.models import Module
from app.schemas.module_schemas import CreateModule, UpdateModule


def create_module_db(db: Session, module: CreateModule):
    new_module = Module(
        number=module.number,
        name=module.name,
        description=module.description,
        subject_id=module.subject_id
    )

    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


def update_module_db(db: Session, module: Module, module_data: UpdateModule):
    for field, value in module_data:
        if value:
            setattr(module, field, value)

    db.commit()
    db.refresh(module)


def select_modules_db(db: Session):
    return db.query(Module).all()


def select_module_by_id_db(db: Session, module_id: int):
    return db.query(Module).filter(Module.id == module_id).first()


def select_modules_by_subject_id_db(db: Session, subject_id):
    return db.query(Module).filter(Module.subject_id == subject_id).all()


def delete_module_db(db: Session, module: Module):
    db.delete(module)
    db.commit()
