from sqlalchemy.ext.asyncio import AsyncSession

import api.models.line as line_model
import  api.schemas.line as line_schema

from typing import List, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result


async def create_task(
    db: AsyncSession, task_create: line_schema.LinePush
) -> line_model.Task:
    task = line_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

def add_message(
    db: AsyncSession, line_add: line_schema.LineGetMessage
) -> line_model.Message:
    message =line_model.Message(**line_add.dict())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message



# async def get_tasks_with_done(db: AsyncSession) -> List[Tuple[int, str, bool]]:
    # result: Result = await (
        # db.execute(
            # select(
                # line_model.Task.id,
                # line_model.Task.text_message,
                # line_model.Done.id.isnot(None).label("Done"),
            # ).outerjoin(line_model.Done)
        # )
    # )
    # return result.all()