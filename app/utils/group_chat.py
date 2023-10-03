def set_last_messages_dict(messages_obj):
    messages_data = {"messages": []}

    for message in messages_obj:
        message_data = {
            "messageId": message.id,
            "messageText": message.message,
            "messageType": message.message_type.value,
            "messageFixed": message.fixed,
            "messageDatetime": message.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
            "groupId": message.group_id,
            "senderId": message.sender_id,
            "senderType": message.sender_type.value,
            "readBy": message.read_by.split(", ") if message.read_by else [],
            "answers": [],
            "attachFiles": []
        }

        for answer in message.group_chat_answer:

            answer_data = {
                "answerId": answer.id,
                "answer": answer.message,
                "answerDatetime": answer.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
                "senderId": answer.sender_id,
                "senderType": answer.sender_type.value,
                "readBy": answer.read_by.split(", ") if answer.read_by else [],
                "attachFiles": []
            }

            for file in answer.attach_file:
                file_data = {
                    "fileId": file.id,
                    "filePath": file.file_path,
                    "mimeType": file.mime_type,
                    "fileName": file.filename,
                    "fileSize": file.size
                }
                answer_data["attachFiles"].append(file_data)

            message_data["answers"].append(answer_data)

        for file in message.attach_file:
            file_data = {
                "fileId": file.id,
                "filePath": file.file_path,
                "mimeType": file.mime_type,
                "fileName": file.filename,
                "fileSize": file.size
            }
            message_data["attachFiles"].append(file_data)

        messages_data["messages"].append(message_data)
    return messages_data


def set_last_message_dict(message_obj):
    attach_files = []
    if message_obj.fileIds:
        file_ids = message_obj.fileIds.split(",") if message_obj.fileIds else []
        file_paths = message_obj.filePaths.split(",") if message_obj.filePaths else []
        mime_types = message_obj.mimeTypes.split(",") if message_obj.mimeTypes else []
        file_names = message_obj.fileNames.split(",") if message_obj.fileNames else []
        file_sizes = message_obj.fileSizes.split(",") if message_obj.fileSizes else []

        for file_id, file_path, mime_type, filename, file_size in zip(
                file_ids, file_paths, mime_types, file_names, file_sizes
        ):
            attach_files.append({
                "fileId": int(file_id),
                "filePath": file_path,
                "mimeType": mime_type,
                "fileName": filename,
                "fileSize": file_size,
            })

    message = {
        "messageId": message_obj.id,
        "messageText": message_obj.message,
        "messageType": message_obj.message_type.value,
        "messageFixed": message_obj.fixed,
        "messageDatetime": message_obj.datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "groupId": message_obj.group_id,
        "senderId": message_obj.sender_id,
        "senderType": message_obj.sender_type.value,
        "readBy": message_obj.read_by.split(", ") if message_obj.read_by else [],
        "attachFiles": attach_files
    }

    return message


def set_last_answer_dict(answer_obj):
    attach_files = []

    if answer_obj:
        file_ids = answer_obj.fileIds.split(",") if answer_obj.fileIds else []
        file_paths = answer_obj.filePaths.split(",") if answer_obj.filePaths else []
        mime_types = answer_obj.mimeTypes.split(",") if answer_obj.mimeTypes else []
        file_names = answer_obj.fileNames.split(",") if answer_obj.fileNames else []
        file_sizes = answer_obj.fileSizes.split(",") if answer_obj.fileSizes else []

        for file_id, file_path, mime_type, filename, file_size in zip(
                file_ids, file_paths, mime_types, file_names, file_sizes
        ):
            attach_files.append({
                "fileId": int(file_id),
                "filePath": file_path,
                "mimeType": mime_type,
                "fileName": filename,
                "fileSize": file_size
            })

    answer = {
        "answerId": answer_obj[0].id,
        "answerText": answer_obj[0].message,
        "answerDatetime": answer_obj[0].datetime_message.strftime("%d.%m.%Y %H:%M:%S"),
        "messageId": answer_obj[0].group_chat.id,
        "senderId": answer_obj[0].sender_id,
        "senderType": answer_obj[0].sender_type,
        "readBy": answer_obj[0].read_by.split(", ") if answer_obj[0].read_by else [],
        "attachFiles": attach_files
    }

    return answer
