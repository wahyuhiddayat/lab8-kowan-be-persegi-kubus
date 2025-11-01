import json
import requests
import os

gateway_url = os.environ.get("OPENFAAS_URL", "http://127.0.0.1:8080")

def handle(event, context):
    try:
        body = json.loads(event.body) if event.body else {}
        rusuk = body.get('rusuk')
        
        if rusuk is None:
            return {"statusCode": 400, "body": json.dumps({"error": "Parameter 'rusuk' harus diisi"})}
        
        try:
            rusuk_float = float(rusuk)
        except (ValueError, TypeError):
            return {"statusCode": 400, "body": json.dumps({"error": "Parameter 'rusuk' harus berupa angka"})}
            
        if rusuk_float < 0:
            return {"statusCode": 400, "body": json.dumps({"error": "Parameter 'rusuk' tidak boleh negatif"})}
        
        persegi_payload = json.dumps({"sisi": rusuk_float})
        persegi_url = f"{gateway_url}/function/luas-persegi"
        
        # Kirim request dengan header Content-Type
        response = requests.post(
            persegi_url, 
            data=persegi_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Parse response
        if response.status_code != 200:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": "Gagal memanggil service luas-persegi",
                    "detail": response.text,  # JSON string
                    "status_code_received": response.status_code
                })
            }
        
        # Parse successful response
        response_data = response.json()
        luas_sisi = response_data.get("luas")
        
        if luas_sisi is None:
            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": "Response dari luas-persegi tidak valid",
                    "response": response.text
                })
            }
        
        luas_permukaan = 6 * luas_sisi
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "luas_permukaan_kubus": luas_permukaan,
                "rusuk": rusuk_float,
                "luas_sisi": luas_sisi
            })
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal server error: {str(e)}"})
        }