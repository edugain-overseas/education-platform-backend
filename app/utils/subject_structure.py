def set_subject_structure(subject_data):
    modules_dict = {}
    for result in subject_data:
        module_id = result.module_id

        lesson_data = {
            "lesson_id": result.lesson_id,
            "lesson_type": result.lesson_type,
            "lesson_number": result.lesson_number,
            "lesson_title": result.lesson_title,
            "lesson_desc": result.lesson_desc,
            "lesson_date": result.lesson_date
        }

        if module_id in modules_dict:
            modules_dict[module_id]["module_lessons"].append(lesson_data)

        else:
            modules_dict[module_id] = {
                "module_id": module_id,
                "module_name": result.module_name,
                "module_number": result.module_number,
                "module_desc": result.module_desc,
                "module_lessons": [lesson_data]
            }

    return list(modules_dict.values())
