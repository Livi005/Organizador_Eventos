import json
from datetime import datetime

def registrar_feedback(evento_id, feedback, usuario='anonimo', log_path='logs_feedback.jsonl'):
    entrada = {
        "timestamp": datetime.utcnow().isoformat(),
        "evento_id": evento_id,
        "usuario": usuario,
        "feedback": feedback
    }
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada) + "\n")

def cargar_logs_feedback(log_path='logs_feedback.jsonl'):
    feedbacks = {}
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for linea in f:
                entrada = json.loads(linea)
                eid = entrada['evento_id']
                fb = entrada['feedback']
                feedbacks[eid] = fb
    except FileNotFoundError:
        pass
    return feedbacks