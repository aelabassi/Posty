from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

    def to_dict(self, save_fs=False):
        """ Return dictionary representation of object """
        new_dict = self.model_dump()
        if save_fs:
            new_dict["__class__"] = self.__class__.__name__
        return new_dict