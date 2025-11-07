import boto3
import json

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # Manejar body que puede venir como dict o string
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
    
    nombre_bucket = body.get('nombre_bucket')
    nombre_directorio = body.get('nombre_directorio')
    
    if not nombre_bucket or not nombre_directorio:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'nombre_bucket y nombre_directorio son requeridos'})
        }
    
    # Asegurar que el nombre del directorio termine con /
    if not nombre_directorio.endswith('/'):
        nombre_directorio += '/'
    
    try:
        s3 = boto3.client('s3')
        
        # Crear objeto vacío que representa el directorio
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=nombre_directorio
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'mensaje': 'Directorio creado exitosamente',
                'bucket': nombre_bucket,
                'directorio': nombre_directorio,
                'etag': response['ETag']
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