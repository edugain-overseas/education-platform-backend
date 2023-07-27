def set_last_messages_dict(messages_obj):
    messages_data = {"messages": []}

    for message in messages_obj:
        message_data = {
            "message_id": message.id,
            "message_text": message.message,
            "message_type": message.message_type.value,
            "message_fixed": message.fixed,
            "message_datetime": message.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
            "group_id": message.group_id,
            "sender_id": message.sender_id,
            "sender_type": message.sender_type.value,
            "read_by": message.read_by.split(", ") if message.read_by else [],
            "answers": [],
            "attach_files": []
        }

        for answer in message.group_chat_answer:

            answer_data = {
                "answer_id": answer.id,
                "answer": answer.message,
                "answer_datetime": answer.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
                "sender_id": answer.sender_id,
                "sender_type": answer.sender_type.value,
                "read_by": answer.read_by.split(", ") if answer.read_by else [],
                "attach_file": []

            }

            for file in answer.attach_file:
                file_data = {
                    "fileId": file.id,
                    "file_path": file.file_path,
                    "mime_type": file.mime_type
                }
                answer_data["attach_file"].append(file_data)

            message_data["answers"].append(answer_data)

        for file in message.attach_file:
            file_data = {
                "fileId": file.id,
                "file_path": file.file_path,
                "mime_type": file.mime_type
            }
            message_data["attach_files"].append(file_data)

        messages_data["messages"].append(message_data)
    return messages_data


def set_last_message_dict(message_obj):
    attach_files = []
    if message_obj.fileIds:
        file_ids = message_obj.fileIds.split(",")
        file_paths = message_obj.filePaths.split(",")
        mime_types = message_obj.mimeTypes.split(",")

        for file_id, file_path, mime_type in zip(file_ids, file_paths, mime_types):
            attach_files.append({
                "fileId": int(file_id),
                "file_path": file_path,
                "mime_type": mime_type
            })

    message = {
        "message_id": message_obj.id,
        "message_text": message_obj.message,
        "message_type": message_obj.message_type.value,
        "message_fixed": message_obj.fixed,
        "message_datetime": message_obj.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "group_id": message_obj.group_id,
        "sender_id": message_obj.sender_id,
        "sender_type": message_obj.sender_type.value,
        "read_by": message_obj.read_by.split(", ") if message_obj.read_by else [],
        "attach_files": attach_files
    }

    return message


def set_last_answer_dict(answer_obj):
    attach_files = []
    if answer_obj:
        file_ids = answer_obj.fileIds.split(",") if answer_obj.fileIds else []
        file_paths = answer_obj.filePaths.split(",") if answer_obj.filePaths else []
        mime_types = answer_obj.mimeTypes.split(",") if answer_obj.mimeTypes else []

        for file_id, file_path, mime_type in zip(file_ids, file_paths, mime_types):
            attach_files.append({
                "fileId": int(file_id),
                "file_path": file_path,
                "mime_type": mime_type
            })

    answer = {
        "answer_id": answer_obj[0].id,
        "answer_text": answer_obj[0].message,
        "answer_datetime": answer_obj[0].datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "message_id": answer_obj[0].group_chat.id,
        "sender_id": answer_obj[0].sender_id,
        "sender_type": answer_obj[0].sender_type,
        "read_by": answer_obj[0].read_by.split(", ") if answer_obj[0].read_by else [],
        "attach_files": attach_files
    }

    return answer
