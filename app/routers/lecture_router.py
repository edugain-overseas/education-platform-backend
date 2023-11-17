from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.celery import confirm_lecture_in_journal
from app.crud.lecture_crud import (check_lecture_db, create_attribute_base_db, create_attribute_file_db,
                                   create_attribute_file_with_description_db, create_attribute_link_db,
                                   create_lecture_db, delete_attribute_db, delete_attribute_file_db,
                                   delete_attribute_link_db, get_attribute_db, get_attribute_file_by_path_db,
                                   get_attribute_file_db, get_attribute_link_db, get_lecture_db, update_attribute_db)
from app.models import User
from app.schemas.lecture_schemas import (AttributeBase, AttributeFile, AttributeFiles, AttributeHomeWork,
                                         AttributeImages, AttributeLinks, UpdateAttributeBase, UpdateAttributeFile,
                                         UpdateAttributeFiles, UpdateAttributeHomeWork, UpdateAttributeImages,
                                         UpdateAttributeLinks)
from app.session import get_db
from app.utils.lesson_utils import get_lecture_attributes_info, get_lesson_base_info
from app.utils.save_images import delete_file, save_lesson_file
from app.utils.token import get_current_user

router = APIRouter()


@router.post("/lecture/create")
async def create_lecture(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        return create_lecture_db(db=db, lesson_id=lesson_id)
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/upload/file")
async def upload_lecture_file(
        file: UploadFile = File(...),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        filepath = save_lesson_file(file)
        return {"fileName": file.filename, "filePath": filepath, "fileSize": file.size}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/lecture/delete/section")
async def delete_attribute(
        attribute_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)

        if attribute.lecture_file:
            for file in attribute.lecture_file:
                delete_file(file.file_path)
                delete_attribute_file_db(db=db, file=file)

        if attribute.lecture_link:
            for link in attribute.lecture_link:
                delete_attribute_link_db(db=db, link=link)

        delete_attribute_db(db=db, attribute=attribute)
        return {"message": "Section have been deleted"}

    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.delete("/lecture/delete/section-file")
async def delete_attribute_file(
        file_path: str,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        file = get_attribute_file_by_path_db(db=db, file_path=file_path)
        delete_file(file.file_path)
        delete_attribute_file_db(db=db, file=file)
        return {"message": "File have been deleted"}
    else:
        HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/create/text")
async def create_text_attribute(
        lecture_id: int,
        item: AttributeBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        create_attribute_base_db(
            db=db,
            lecture_id=lecture_id,
            attr_type=item.attributeType,
            attr_title=item.attributeTitle,
            attr_text=item.attributeText,
            attr_number=item.attributeNumber,
            hided=item.hided
        )
        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/lecture/update/text")
async def update_text_attribute(
        attribute_id: int,
        item: UpdateAttributeBase,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)
        update_attribute_db(
            db=db,
            attribute=attribute,
            title=item.attributeTitle,
            text=item.attributeText,
            number=item.attributeNumber,
            hided=item.hided
        )
        return {"message": "Attribute have been updated"}


@router.post("/lecture/create/file")
async def create_file_attribute(
        lecture_id: int,
        item: AttributeFile,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = create_attribute_base_db(
            db=db,
            lecture_id=lecture_id,
            attr_type=item.attributeType,
            attr_title=item.attributeTitle,
            attr_text=item.attributeText,
            attr_number=item.attributeNumber,
            hided=item.hided
        )

        create_attribute_file_db(
            db=db,
            attribute_id=attribute.id,
            filename=item.fileName,
            file_size=item.fileSize,
            file_path=item.filePath,
            download_allowed=item.downloadAllowed
        )
        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/lecture/update/file")
async def update_file_attribute(
        attribute_id: int,
        item: UpdateAttributeFile,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)
        update_attribute_db(
            db=db,
            attribute=attribute,
            title=item.attributeTitle,
            text=item.attributeText,
            number=item.attributeNumber,
            hided=item.hided
        )

        file = get_attribute_file_db(db=db, file_id=attribute.lecture_file[0].id)
        delete_file(attribute.lecture_file[0].file_path)
        delete_attribute_file_db(db=db, file=file)

        create_attribute_file_db(
            db=db,
            attribute_id=attribute.id,
            filename=item.fileName,
            file_size=item.fileSize,
            file_path=item.filePath,
            download_allowed=item.downloadAllowed
        )

        return {"message": "Attribute have been updated"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/create/files")
async def create_files_attribute(
        lecture_id: int,
        item: AttributeFiles,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = create_attribute_base_db(
            db=db,
            lecture_id=lecture_id,
            attr_type=item.attributeType,
            attr_title=item.attributeTitle,
            attr_text=item.attributeText,
            attr_number=item.attributeNumber,
            hided=item.hided
        )

        for file in item.attributeFiles:
            create_attribute_file_db(
                db=db,
                attribute_id=attribute.id,
                filename=file.fileName,
                file_path=file.filePath,
                file_size=file.fileSize,
                download_allowed=file.downloadAllowed,
            )

        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/lecture/update/files")
async def update_files_attribute(
        attribute_id: int,
        item: UpdateAttributeFiles,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)
        update_attribute_db(
            db=db,
            attribute=attribute,
            title=item.attributeTitle,
            text=item.attributeText,
            number=item.attributeNumber,
            hided=item.hided
        )

        for att_file in attribute.lecture_file:
            file = get_attribute_file_db(db=db, file_id=att_file.id)
            delete_attribute_file_db(db=db, file=file)

        for file in item.attributeFiles:
            create_attribute_file_db(
                db=db,
                attribute_id=attribute.id,
                filename=file.fileName,
                file_path=file.filePath,
                file_size=file.fileSize,
                download_allowed=file.downloadAllowed,
            )

        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/create/images")
async def create_images_attribute(
        lecture_id: int,
        item: AttributeImages,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = create_attribute_base_db(
            db=db,
            lecture_id=lecture_id,
            attr_type=item.attributeType,
            attr_title=item.attributeTitle,
            attr_text=item.attributeText,
            attr_number=item.attributeNumber,
            hided=item.hided
        )

        for image in item.attributeImages:
            create_attribute_file_with_description_db(
                db=db,
                attribute_id=attribute.id,
                filename=image.imageName,
                file_path=image.imagePath,
                file_size=image.imageSize,
                file_description=image.imageDescription,
                download_allowed=image.downloadAllowed,
            )
        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/lecture/update/images")
async def update_images_attribute(
        attribute_id: int,
        item: UpdateAttributeImages,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)
        update_attribute_db(
            db=db,
            attribute=attribute,
            title=item.attributeTitle,
            text=item.attributeText,
            number=item.attributeNumber,
            hided=item.hided
        )

        for att_file in attribute.lecture_file:
            file = get_attribute_file_db(db=db, file_id=att_file.id)
            delete_attribute_file_db(db=db, file=file)

        for image in item.attributeImages:
            create_attribute_file_with_description_db(
                db=db,
                attribute_id=attribute.id,
                filename=image.imageName,
                file_path=image.imagePath,
                file_size=image.imageSize,
                file_description=image.imageDescription,
                download_allowed=image.downloadAllowed,
            )
        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/create/link")
async def create_link_attribute(
        lecture_id: int,
        item: AttributeLinks,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = create_attribute_base_db(
            db=db,
            lecture_id=lecture_id,
            attr_type=item.attributeType,
            attr_title=item.attributeTitle,
            attr_text=item.attributeText,
            attr_number=item.attributeNumber,
            hided=item.hided
        )

        for link in item.attributeLinks:
            create_attribute_link_db(db=db, link=link.link, anchor=link.anchor, attribute_id=attribute.id)

        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/lecture/update/link")
async def update_link_attribute(
        attribute_id: int,
        item: UpdateAttributeLinks,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)
        update_attribute_db(
            db=db,
            attribute=attribute,
            title=item.attributeTitle,
            text=item.attributeText,
            number=item.attributeNumber,
            hided=item.hided
        )

        for attr_link in attribute.lecture_link:
            link = get_attribute_link_db(db=db, link_id=attr_link.id)
            delete_attribute_link_db(db=db, link=link)

        for new_link in item.attributeLinks:
            create_attribute_link_db(db=db, attribute_id=attribute.id, link=new_link.link, anchor=new_link.anchor)

        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.post("/lecture/create/homework")
async def create_homework_attribute(
        lecture_id: int,
        item: AttributeHomeWork,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = create_attribute_base_db(
            db=db,
            lecture_id=lecture_id,
            attr_type=item.attributeType,
            attr_title=item.attributeTitle,
            attr_text=item.attributeText,
            attr_number=item.attributeNumber,
            hided=item.hided
        )

        if item.attributeFiles:
            for file in item.attributeFiles:
                create_attribute_file_db(
                    db=db,
                    filename=file.fileName,
                    file_path=file.filePath,
                    file_size=file.fileSize,
                    download_allowed=file.downloadAllowed,
                    attribute_id=attribute.id
                )

        if item.attributeLinks:
            for link in item.attributeLinks:
                create_attribute_link_db(
                    db=db,
                    link=link.link,
                    anchor=link.anchor,
                    attribute_id=attribute.id
                )

        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.put("/lecture/update/homework")
async def update_homework_attribute(
        attribute_id: int,
        item: UpdateAttributeHomeWork,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.teacher or user.moder:
        attribute = get_attribute_db(db=db, attr_id=attribute_id)
        update_attribute_db(
            db=db,
            attribute=attribute,
            title=item.attributeTitle,
            text=item.attributeText,
            number=item.attributeNumber,
            hided=item.hided
        )

        if item.attributeLinks:
            for attr_link in attribute.lecture_link:
                link = get_attribute_link_db(db=db, link_id=attr_link.id)
                delete_attribute_link_db(db=db, link=link)

            for new_link in item.attributeLinks:
                create_attribute_link_db(
                    db=db,
                    attribute_id=attribute.id,
                    link=new_link.link,
                    anchor=new_link.anchor
                )

        if item.attributeFiles:
            for attr_file in attribute.lecture_file:
                file = get_attribute_file_db(db=db, file_id=attr_file.id)
                delete_attribute_file_db(db=db, file=file)

            for new_file in item.attributeFiles:
                create_attribute_file_db(
                    db=db,
                    attribute_id=attribute.id,
                    filename=new_file.fileName,
                    file_path=new_file.filePath,
                    file_size=new_file.fileSize,
                    download_allowed=new_file.downloadAllowed
                )

        return {"message": "Attribute have been saved"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")


@router.get("/lecture/{lesson_id}")
async def get_lecture_data(
        lesson_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    base_info = get_lesson_base_info(db=db, lesson_id=lesson_id)
    lecture = get_lecture_db(db=db, lesson_id=lesson_id)

    if lecture is not None:
        return get_lecture_attributes_info(base_info=base_info, lecture=lecture)
    else:
        return base_info


@router.post("/confirm")
async def config_lecture(
        lecture_id: int,
        student_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    if user.student:
        check_lecture_db(db=db, lecture_id=lecture_id, student_id=student_id)
        confirm_lecture_in_journal.delay(student_id=student_id, lecture_id=lecture_id)
        return {"message": "Lecture have been viewed"}
    else:
        raise HTTPException(status_code=403, detail="Permission denied")
