from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class User(BaseModel):
    name: str
    address: Address

if __name__ == "__main__":
    user = User(name="Bob", address={"street":"朝阳路", "city":"上海", "state":"12", "zip_code":"12321"})