from fastapi import APIRouter
import json
import os

router = APIRouter(tags=["Patates"])

# Yeni endpoint: Tatlı patates sayısını döndür
@router.get("/patates")
async def tatli_patates_sayisi():
    json_path = os.path.join(os.path.dirname(__file__), "gizli_patates.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    tatli = next((p for p in data.get("patatesler", []) if p.get("cesit") == "Tatlı"), None)
    if tatli:
        return {"adet": tatli["sayi"]}
    else:
        return {"adet": 0}