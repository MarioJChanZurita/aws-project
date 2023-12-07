from typing import Union, Annotated
from fastapi import APIRouter, Depends, Request, Response, status, Body, Path, HTTPException
from src.models import Alumno

alumnos = APIRouter(prefix='/alumnos', tags=["Alumnos"])


@alumnos.get("", status_code=status.HTTP_200_OK)
def obtener_alumnos():
    return ALUMNOS

@alumnos.get("/{id}", status_code=status.HTTP_200_OK)
def obtener_alumno(id: int):
    for alumno in ALUMNOS:
        if alumno['id'] == id:
            return alumno
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Alumno no encontrado"
    )
@alumnos.post("", status_code=status.HTTP_201_CREATED)
def agregar_alumnos(alumno: Alumno):
    ALUMNOS.append(alumno.dict())
    return {'id': alumno.id}

@alumnos.put("/{id}", status_code=status.HTTP_200_OK)
def actualizar_alumno(id: int, data: Alumno):
    for alumno in ALUMNOS:
        if alumno['id'] == id:
            alumno.update(data.dict(exclude_defaults=True))
            return alumno
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Alumno no encontrado"
    )

@alumnos.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_alumno(id: int):
    for i, alumno in enumerate(ALUMNOS):
        if alumno['id'] == id:
            ALUMNOS.pop(i)
            return alumno
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Alumno no encontrado"
    )







@students.post("/{id}/fotoPerfil", tags=["Alumnos"])
def upload_foto_perfil(id :int, foto: UploadFile = File(...), db: Session = Depends(get_db)):
    return StudentsService().upload_profile_picture(id, foto, db)

@students.post("/{id}/email", tags=["Alumnos"])
def send_email(id: int, db: Session = Depends(get_db)):
    return StudentsService().send_email(id, db)
    
@students.post("/{id}/session/login", tags=["Alumnos"])
def login(id: int, password: str = Body(embed=True), db: Session = Depends(get_db)):
    return StudentsService().login(id, password, db)
  

@students.post("/{id}/session/verify", tags=["Alumnos"])
def verify(id: int, sessionString:str = Body(embed=True), db: Session = Depends(get_db)):
    return StudentsService().verify_session(id, sessionString, db)
    
@students.post("/{id}/session/logout", tags=["Alumnos"])
def logout(id: int, sessionString: str = Body(embed=True), db: Session = Depends(get_db)):
    return StudentsService().logout(id, sessionString, db)
