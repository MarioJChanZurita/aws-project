from typing import Union, Annotated
from fastapi import APIRouter, Body, File, HTTPException, UploadFile, status, Depends
from src.models import Alumno
from src.services import AlumnoServicio as Servicio
from src.utils import get_db
from sqlalchemy.orm import Session

alumnos = APIRouter(prefix='/alumnos', tags=["Alumnos"])

@alumnos.get("", status_code=status.HTTP_200_OK)
def obtener_alumnos(
    db: Session = Depends(get_db)
):
    return Servicio(db).obtener_alumnos()

@alumnos.get("/{id}", status_code=status.HTTP_200_OK)
def obtener_alumno(
    id: int,
    db: Session = Depends(get_db)
):
    return Servicio(db).obtener_alumno(id)     

@alumnos.post("", status_code=status.HTTP_201_CREATED)
def agregar_alumnos(
    alumno: Alumno,
    db: Session = Depends(get_db)
):
    return Servicio(db).agregar_alumnos(alumno)

@alumnos.put("/{id}", status_code=status.HTTP_200_OK)
def actualizar_alumno(
    id: int, 
    data: Alumno,
    db: Session = Depends(get_db)
):
    return Servicio(db).actualizar_alumno(id, data)

@alumnos.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_alumno(
    id: int,
    db: Session = Depends(get_db)
):
    return Servicio(db).eliminar_alumno(id)

@alumnos.post("/{id}/fotoPerfil", tags=["Alumnos"])
def upload_foto_perfil(
    id :int, 
    foto: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    return Servicio(db).subir_foto_perfil(id, foto)

@alumnos.post("/{id}/email", tags=["Alumnos"])
def enviar_email(
    id: int, 
    db: Session = Depends(get_db)
):
    return Servicio(db).enviar_email(id)
    
@alumnos.post("/{id}/session/login", tags=["Alumnos"])
def login(
    id: int, 
    password: str = Body(embed=True), 
    db: Session = Depends(get_db)
):
    return Servicio(db).login(id, password)
  
@alumnos.post("/{id}/session/verify", tags=["Alumnos"])
def verify(
    id: int, 
    sessionString:str = Body(embed=True), 
    db: Session = Depends(get_db)
):
    return Servicio(db).is_authorize(id, sessionString)
    
@alumnos.post("/{id}/session/logout", tags=["Alumnos"])
def logout(
    id: int, 
    sessionString: str = Body(embed=True),
    db: Session = Depends(get_db)
):
    return Servicio(db).logout(id, sessionString)
