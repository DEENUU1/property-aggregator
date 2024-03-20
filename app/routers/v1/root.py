from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["root"]
)


@router.get("", status_code=200)
def health():
    return {"status": "ok"}
