import src.schemas as Schemas
from src.models import Alumno



class AlumnoService():


    def obtener_alumnos():
        return ALUMNOS

    def obtener_alumno(id: int):
        for alumno in ALUMNOS:
            if alumno['id'] == id:
                return alumno
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )
    
    def agregar_alumnos(alumno: Alumno):
        ALUMNOS.append(alumno.dict())
        return {'id': alumno.id}

    def actualizar_alumno(id: int, data: Alumno):
        for alumno in ALUMNOS:
            if alumno['id'] == id:
                alumno.update(data.dict(exclude_defaults=True))
                return alumno
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )

    def eliminar_alumno(id: int):
        for i, alumno in enumerate(ALUMNOS):
            if alumno['id'] == id:
                ALUMNOS.pop(i)
                return alumno
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alumno no encontrado"
        )

    def upload_profile_picture(self, id: int, photo: UploadFile, db: Session) -> JSONResponse:
        student: Schemas.Alumno = self.obtener_alumno(id, db)
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                tmp.write(photo.file.read())
                file = tmp.name
                filename = photo.filename
                upload_file_to_s3(file, filename)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error al subir imagen"
            )
        student.fotoPerfilUrl = f"https://{env.get('BUCKET_NAME')}.s3.amazonaws.com/{filename}"
        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "fotoPerfilUrl": student.fotoPerfilUrl
            }
        )
            
        
    def send_email(self, id: int, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        publish_message_to_sns(
            topic_arn=env.get("TOPIC_ARN"),
            message=f"Nombre: {student.nombres}\nApellido: {student.apellidos}\nCalificaciones: {student.promedio}"
        )
        return success_response("Correo enviado")
            
        
    def login(self, id: int, password: str, db: Session) -> JSONResponse:
        student: Query[DBStudent] = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alumno no encontrado"
                )
        if student.password != password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña incorrecta"
            )
        sessionString: str = get_random_string(128)
        put_item_to_dynamodb(
            table_name=env.get('DYNAMODB_TABLE'),
            item={
                'id': str(uuid.uuid4()),
                'fecha': int(time.time()),
                'alumnoId': id,
                'active': True,
                'sessionString': sessionString
            }
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "sessionString": sessionString
            }
        )
            
            
        
    def verify_session(self, id: int, sessionString: str, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        response: list[dict] | list = scan_table(
            table_name=env.get('DYNAMODB_TABLE'),
            filter_expression=Attr('sessionString').eq(sessionString)
        )
        if response:
            is_active = response[0].get('active', False)
        if not response or not is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        return success_response("Sesión válida")
        

    def logout(self, id: int, sessionString: str, db: Session) -> JSONResponse:
        student: DBStudent = StudentsService().get_student(id, db)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Alumno no encontrado"
            )
        response: list[dict] = scan_table(
            table_name=env.get('DYNAMODB_TABLE'),
            filter_expression=Attr('sessionString').eq(sessionString)
        )
        id = response[0].get('id', False)
        if not response or not id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sesión inválida"
            )
        update_item_in_dynamodb(
            table_name=env.get('DYNAMODB_TABLE'),
            key={
                'id': id
            },
            update_expression='SET active = :active',
            expression_attribute_values={
                ':active': False
            }
        )
        return success_response("Sesión cerrada")
