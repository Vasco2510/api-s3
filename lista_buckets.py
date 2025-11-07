# lista_objetos_bucket.py (CORREGIDO)
import boto3
import json

def lambda_handler(event, context):
    
    body = event.get('body', {})
    if isinstance(body, str):
        body = json.loads(body)

    nombre_bucket = body.get('bucket')
    
    if not nombre_bucket:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'El campo "bucket" es requerido en el body'})
        }
        
    try:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=nombre_bucket) # Usar v2 es mejor
        
        lista = []
        if 'Contents' in response:
            for obj in response['Contents']:
                lista.append(obj['Key'])

        return {
            'statusCode': 200,
            'body': json.dumps({ # 🔥 CORRECCIÓN: El retorno debe ser un string JSON
                'bucket': nombre_bucket,
                'lista_objetos': lista
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'bucket_solicitado': nombre_bucket})
        }