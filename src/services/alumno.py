from tempfile import NamedTemporaryFile
import time
import uuid
from fastapi import HTTPException, Query, UploadFile, status
from fastapi.responses import JSONResponse
from src.schemas import Alumno as dbAlumno
from src.models import Alumno
from sqlalchemy.orm import Session
from src.utils import AWS, AWSServices
from src.utils.const import BUCKET_NAME, DYNAMODB_TABLE, SNS_TOPIC_ARN
from src.utils.helpers import success_response, generate_token
from boto3.dynamodb.conditions import Attr


class AlumnoServicio():

    def __init__(self, db: Session):
        self.db = db

    def obtener_alumnos(self):
        alumnos: dbAlumno | None = self.db.query(dbAlumno).all()
        return alumnos

    def obtener_alumno(self, id: int):
        alumno: dbAlumno | None = self.db.query(dbAlumno).filter(dbAlumno.id == id).first()
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        return alumno

    def agregar_alumnos(self, alumno: Alumno):
        alumno: dbAlumno = dbAlumno(**alumno.model_dump())
        self.db.add(alumno)
        self.db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "id": alumno.id
            }
        )

    def actualizar_alumno(self, id: int, item: Alumno):
        item = item.model_dump()
        item.pop("id", None)
        alumno: Query[dbAlumno] = self.db.query(dbAlumno).filter(dbAlumno.id == id)
        if alumno:
            alumno.update(item)
            self.db.commit()
            return success_response("Alumno actualizado")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )

    def eliminar_alumno(self, id: int):
        alumno: Query[dbAlumno] = self.obtener_alumno(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        self.db.delete(alumno)
        self.db.commit()
        return success_response("Alumno eliminado")

    def subir_foto_perfil(self, id: int, foto: UploadFile):
        s3 = AWS(AWSServices.s3)
        alumno = self.obtener_alumno(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Alumno no encontrado"
            )
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                tmp.write(foto.file.read())
                s3.subir(tmp.name, foto.filename)
        except Exception as ex:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=str(ex)
            )
        alumno.fotoPerfilUrl = "https://{buket_name}.s3.amazonaws.com/{filename}".format(
            buket_name=BUCKET_NAME,
            filename=foto.filename
        )
        self.db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"fotoPerfilUrl": alumno.fotoPerfilUrl}
        )
              
    def enviar_email(self, id: int):
        sns = AWS(AWSServices.sns)
        alumno = self.obtener_alumno(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        sns.publicar_msg(
            topic_arn=SNS_TOPIC_ARN,
            message="Nombre: {nombre}\nApellido: {apellidos}\nCalificaciones: {promedio}".format(
                nombre=alumno.nombres,
                apellidos=alumno.apellidos,
                promedio=alumno.promedio
            )
        )
        return success_response("Correo enviado")

    def login(self, id: int, password: str):
        dynamodb = AWS(AWSServices.dynamodb)
        alumno: Query[dbAlumno] = self.obtener_alumno(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        if alumno.password != password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña incorrecta"
            )
        token: str = generate_token(128)
        sesion = {
            'id': str(uuid.uuid4()),
            'fecha': int(time.time()),
            'alumnoId': id,
            'active': True,
            'sessionString': token
        }
        dynamodb.agregar_dynamodb(
            table_name=DYNAMODB_TABLE,
            item=sesion
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={ "sessionString": token }
        )
            
    def is_authorize(self, id: int, token: str):
        dynamodb = AWS(AWSServices.dynamodb)
        alumno: dbAlumno = self.obtener_alumno(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        sesion: list[dict] | list = dynamodb.escanear_tabla(
            table_name=DYNAMODB_TABLE,
            filter_expression=Attr('sessionString').eq(token)
        )
        is_active = sesion and sesion[0].get('active', False)
        if not is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        return success_response("Sesión válida")
        
    def logout(self, id: int, sessionString: str):
        dynamodb = AWS(AWSServices.dynamodb)
        alumno: dbAlumno = self.obtener_alumno(id)
        if not alumno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        sesion: list[dict] = dynamodb.escanear_tabla(
            table_name=DYNAMODB_TABLE,
            filter_expression=Attr('sessionString').eq(sessionString)
        )
        id = sesion and sesion[0].get('id', False)
        if not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        dynamodb.actualizar(
            table_name=DYNAMODB_TABLE,
            key={ 'id': id },
            update_expression='SET active = :active',
            expression_attribute_values={':active': False}
        )
        return success_response("Sesión cerrada")
