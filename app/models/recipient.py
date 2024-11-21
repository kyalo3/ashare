from typing import Any
from pydantic import BaseModel
from bson.objectid import ObjectId
from app.database import recipient_collection
"""
recipient module
"""


class RecipientBase(BaseModel):
    """ base model for recipient """
    first_name: str
    last_name: str
    email: str
    id_no: str
    phone_number: str
    gender: str
    


class RecipientCreate(RecipientBase):
    """ model for creating a recipient """
    pass


class Recipient(RecipientBase):
    """ class to represent a recipient """
    id: str
    user_id: str

    class Config:
        """pydantic configuration for recipient """
        from_attributes = True


def recipient_helper(recipient: Any) -> dict:
    """Helper function to transform recipient document to dictionary"""
    return {
        "user_id": recipient["user_id"],
        "first_name": recipient["first_name"],
        "last_name": recipient["last_name"],
        "email": recipient["email"],
        "id_no": recipient["id_no"],
        "phone_number": recipient["phone_number"],  # Add this line
        "gender": recipient["gender"],
    }


async def create_recipient(recipient: RecipientCreate, user_id: str):
    """Create a new recipient"""
    recipient_dict = recipient.dict()
    recipient_dict['user_id'] = user_id
    new_recipient = await recipient_collection.insert_one(recipient_dict)
    return recipient_helper(await recipient_collection.find_one({"_id": new_recipient.inserted_id}))


async def get_recipient_by_id(recipient_id: str):
    """Get recipient by ID"""
    recipient = await recipient_collection.find_one({"_id": ObjectId(recipient_id)})
    if recipient:
        return recipient_helper(recipient)

async def get_recipient_by_user_id(user_id: str):
    """Get recipient by user ID"""
    recipients = []
    async for recipient in recipient_collection.find({"user_id": user_id}):
        recipients.append(recipient_helper(recipient))
    return recipients

async def update_recipient(recipient_id: str, recipient: RecipientCreate):
    """Update recipient by ID"""
    updated_recipient = await recipient_collection.update_one({"_id": ObjectId(recipient_id)}, {"$set": recipient.dict()})
    if updated_recipient:
        return await recipient_collection.find_one({"_id": ObjectId(recipient_id)})
    return None

async def delete_recipient(recipient_id: str):
    """Delete recipient by ID"""
    deleted_recipient = await recipient_collection.delete_one({"_id": ObjectId(recipient_id)})
    if deleted_recipient:
        return True
    return False

async def get_recipients():
    """Get all recipients"""
    recipients = []
    async for recipient in recipient_collection.find():
        recipients.append(recipient_helper(recipient))
    return recipients

async def get_recipient_by_name(name: str):
    """Get recipient by name"""
    recipient = await recipient_collection.find_one({"name": name})
    if recipient:
        return recipient_helper(recipient)
    return None

async def get_recipient_by_user_id_and_name(user_id: str, name: str):
    """Get recipient by user ID and name"""
    recipient = await recipient_collection.find_one({"user_id":
                                                        user_id, "name": name})
    if recipient:
        return recipient_helper(recipient)
    return None

async def get_recipient_by_id_and_user_id(recipient_id: str, user_id: str):
    """Get recipient by ID and user ID"""
    recipient = await recipient_collection.find_one({"_id": ObjectId(recipient_id), "user_id": user_id})
    if recipient:
        return recipient_helper(recipient)
    return None
