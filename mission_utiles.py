from pydantic import BaseModel

VALID_STATUS = ("NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED")

class MissionCreateBody(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int

class MissionUpdateBody(BaseModel):
    title: str | None = None
    description: str | None = None
    location: str | None = None
    difficulty: int
    importance: int


class InvalidDifficultyOrImportance(Exception):
    pass

# class InvalidImportance(Exception):
#     pass


def check_difficulty_and_importance(body:MissionCreateBody) -> bool:
    """docstring"""
    if body.difficulty >= 1 and body.difficulty <= 10:
        valid = True
    else:
        raise InvalidDifficultyOrImportance
    
    if body.importance >= 1 and body.importance <= 10:
        valid = True
    else:
        raise InvalidDifficultyOrImportance
    
    return valid
    
