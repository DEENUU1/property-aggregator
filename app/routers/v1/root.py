from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["root"]
)


@router.get("")
def health():
    """ Check if the service is running correctly """
    return {"status": "ok"}
