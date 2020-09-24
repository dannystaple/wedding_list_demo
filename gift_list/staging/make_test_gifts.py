from ..models.gifts import GiftList
from ..models import settings

def make_test_gifts():
    gl = GiftList(settings.get_db_connection())
    gl.add(9)
    gl.add(13)
    gl.add(19)
    gl.purchase(13)

if __name__ == "__main__":
    make_test_gifts()