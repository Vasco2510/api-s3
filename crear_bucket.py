import boto3
import json
import uuid

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # Manejar body que puede venir como dict o string
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
    
    nombre_bucket = body.get('nombre_bucket')
    
    if not nombre_bucket:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'nombre_bucket es requerido'})
        }
    
    # Agregar sufijo único para evitar colisiones
    nombre_bucket_unico = f"{nombre_bucket}-{str(uuid.uuid4())[:8]}"
    
    try:
        s3 = boto3.client('s3')
        response = s3.create_bucket(
            Bucket=nombre_bucket_unico,
            CreateBucketConfiguration={
                'LocationConstraint': 'us-east-1'
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'mensaje': 'Bucket creado exitosamente',
                'nombre_bucket': nombre_bucket_unico,
                'location': response['Location']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }