from fastapi import APIRouter, status, Depends
from src.models import Profesor
from src.services import ProfesorServicio as Servicio
from sqlalchemy.orm import Session
from src.utils import get_db

PROFESORES = []

profesores = APIRouter(prefix='/profesores', tags=["Profesores"], include_in_schema=False)


@profesores.get("", status_code=status.HTTP_200_OK)
def obtener_profesores(
    db: Session = Depends(get_db)
):
    return Servicio(db).obtener_profesores()
    

@profesores.get("/{id}", status_code=status.HTTP_200_OK)
def obtener_profesor(
    id: int,
    db: Session = Depends(get_db)
):
    return Servicio(db).obtener_profesor(id)

@profesores.post("", status_code=status.HTTP_201_CREATED)
def agregar_profesores(
    profesor: Profesor,
    db: Session = Depends(get_db)
):
    return Servicio(db).agregar_profesores(profesor)

@profesores.put("/{id}", status_code=status.HTTP_200_OK)
def actualizar_profesor(
    id: int, 
    data: Profesor,
    db: Session = Depends(get_db)
):
    return Servicio(db).actualizar_profesor(id, data)

@profesores.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_profesor(
    id: int,
    db: Session = Depends(get_db)
):
    return Servicio(db).eliminar_profesor(id)
