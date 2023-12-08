from fastapi import HTTPException, status
from fastapi.params import Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.models import Profesor 
from src.schemas import Profesor as dbProfesor
from src.utils.helpers import success_response


class ProfesorServicio:

    def __init__(self, db: Session):
        self.db = db

    def obtener_profesores(self):
        profesores: dbProfesor | None = self.db.query(dbProfesor).all()
        return profesores

    def obtener_profesor(self, id: int):
        profesor: dbProfesor | None = self.db.query(dbProfesor).filter(dbProfesor.id == id).first()
        if not profesor:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Profesor no encontrado"
                )
        return profesor

    def agregar_profesores(self, profesor: Profesor):
        profesor: dbProfesor = dbProfesor(**profesor.model_dump())
        self.db.add(profesor)
        self.db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": profesor.id
            }
        )

    def actualizar_profesor(self, id: int, item: Profesor):
        item = item.model_dump()
        item.pop("id", None)
        profesor: Query[dbProfesor] = self.db.query(dbProfesor).filter(dbProfesor.id == id)
        if profesor:
            profesor.update(item)
            self.db.commit()
            return success_response("Profesor actualizado")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesor no encontrado"
        )

    def eliminar_profesor(self, id: int):
        profesor: Query[dbProfesor] = self.obtener_profesor(id)
        if not profesor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesor no encontrado"
            )
        self.db.delete(profesor)
        self.db.commit()
        return success_response("Profesor eliminado")