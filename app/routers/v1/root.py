from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["root"]
)


@router.get("", status_code=200)
def health():
    """ Check if the service is running correctly """
    return {"status": "ok"}


