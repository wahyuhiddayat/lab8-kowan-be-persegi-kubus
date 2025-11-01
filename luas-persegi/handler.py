import json

def handle(event, context):
    """
    FaaS function buat ngitung luas persegi.
    Input: {"sisi": <number>}
    """
    try:
        body = json.loads(event.body) if event.body else {}
        sisi = body.get('sisi')
        
        if sisi is None:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Parameter 'sisi' harus diisi"})
            }
        
        try:
            sisi_float = float(sisi)
        except (ValueError, TypeError):
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Parameter 'sisi' harus berupa angka"})
            }

        if sisi_float < 0:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Sisi tidak boleh negatif"})
            }
        
        luas = sisi_float * sisi_float
        
        return {
            "statusCode": 200,
            "body": json.dumps({"sisi": sisi_float, "luas": luas})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Input harus dalam format JSON yang valid"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Internal server error: {str(e)}"})
        }