from pydantic import BaseModel, ConfigDict


class TransactionSchema(BaseModel):
    id: int
    user_id: int
    amount: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class TransactionCreateRequest(BaseModel):
    user_id: int
    amount: int
    status: str = "pending"
