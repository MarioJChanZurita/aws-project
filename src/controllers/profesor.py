from typing import Annotated, Union
from fastapi import APIRouter, Request, status, Body, Path, HTTPException
from src.models import Profesor

PROFESORES = []

profesores = APIRouter(prefix='/profesores', tags=["Profesores"], include_in_schema=False)


@profesores.get("", status_code=status.HTTP_200_OK)
def obtener_profesores():
    return PROFESORES

@profesores.get("/{id}", status_code=status.HTTP_200_OK)
def obtener_profesor(id: int):
    for profesor in PROFESORES:
        if profesor['id'] == id:
            return profesor
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Profesor no encontrado"
    )

@profesores.post("", status_code=status.HTTP_201_CREATED)
def agregar_profesores(profesor: Profesor):
    PROFESORES.append(profesor.dict())
    return {'id': profesor.id}

@profesores.put("/{id}", status_code=status.HTTP_200_OK)
def actualizar_profesor(id: int, data: Profesor):
    for profesor in PROFESORES:
        if profesor['id'] == id:
            profesor.update(data.dict(exclude_defaults=True))
            return profesor
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Profesor no encontrado"
    )

@profesores.delete("/{id}", status_code=status.HTTP_200_OK)
def eliminar_profesor(id: int):
    for i, profesor in enumerate(PROFESORES):
        if profesor['id'] == id:
            PROFESORES.pop(i)
            return profesor
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Profesor no encontrado"
    )
