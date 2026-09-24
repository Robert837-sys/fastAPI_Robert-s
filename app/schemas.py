from pydantic import BaseModel ,ConfigDict
from datetime import datetime

    
class PostBase(BaseModel):
    title: str
    content: str
    published:bool=True  
    
class PostCreate(PostBase):
    pass
    

class Post(PostBase):
    id: int
    created_at:datetime
        
    model_config=ConfigDict(from_attributes=True)