import boto3
import json
import base64
import uuid

def lambda_handler(event, context):
    print("Event recibido:", json.dumps(event))
    
    # Manejar body que puede venir como dict o string
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)
    
    nombre_bucket = body.get('nombre_bucket')
    nombre_archivo = body.get('nombre_archivo')
    contenido_base64 = body.get('contenido_base64')
    directorio = body.get('directorio', '')
    
    if not nombre_bucket or not nombre_archivo or not contenido_base64:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'nombre_bucket, nombre_archivo y contenido_base64 son requeridos'})
        }
    
    try:
        # Decodificar contenido base64
        contenido_binario = base64.b64decode(contenido_base64)
        
        # Construir la ruta completa del archivo
        if directorio:
            if not directorio.endswith('/'):
                directorio += '/'
            ruta_archivo = f"{directorio}{nombre_archivo}"
        else:
            ruta_archivo = nombre_archivo
        
        s3 = boto3.client('s3')
        
        response = s3.put_object(
            Bucket=nombre_bucket,
            Key=ruta_archivo,
            Body=contenido_binario,
            ContentType='application/octet-stream'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'mensaje': 'Archivo subido exitosamente',
                'bucket': nombre_bucket,
                'archivo': ruta_archivo,
                'tamaño': len(contenido_binario),
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