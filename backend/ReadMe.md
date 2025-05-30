Flujo típico de una petición
Petición HTTP llega al router (routes/).

FastAPI valida el body/query/path contra un schema de entrada.

El router extrae dependencias (p. ej. db: Session = Depends(get_db)) y llama al servicio apropiado.

El servicio usa clases de models + sesión (db) para leer/escribir en la base de datos, aplica lógica de negocio.

El servicio retorna un objeto (o Pydantic model), que el router convierte a un schema de salida.

FastAPI serializa ese esquema a JSON y responde al cliente.