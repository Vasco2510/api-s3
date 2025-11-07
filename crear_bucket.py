# crear_bucket.py (CORREGIDO)
import boto3
import json
import uuid

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
    
    nombre_bucket = body.get('nombre_bucket')
    
    if not nombre_bucket:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'nombre_bucket es requerido'})
        }
    
    nombre_bucket_unico = f"{nombre_bucket}-{str(uuid.uuid4())[:8]}"
    
    try:
        s3 = boto3.client('s3')
        
        # 🔥 CORRECCIÓN: 
        # Se elimina CreateBucketConfiguration. 
        # Para 'us-east-1' no se debe especificar LocationConstraint.
        # Si quisieras otra región (ej: 'us-west-2'), la configuración SÍ sería necesaria.
        response = s3.create_bucket(
            Bucket=nombre_bucket_unico
        )
        
        # Obtenemos la URL de ubicación
        location = s3.get_bucket_location(Bucket=nombre_bucket_unico)['LocationConstraint']
        # 'location' puede ser None para us-east-1, o el string de la región
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'mensaje': 'Bucket creado exitosamente',
                'nombre_bucket': nombre_bucket_unico,
                'location': location or 'us-east-1'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }