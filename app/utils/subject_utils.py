def set_subjects_lessons_structure(subject_data):
    modules = {}

    for item in subject_data:
        if item.module_id not in modules:
            modules[item.module_id] = {
                "module_id": item.module_id,
                "module_name": item.module_name,
                "module_number": item.module_number,
                "module_desc": item.module_desc,
                "module_lessons": []
            }

        if item.lesson_title:
            lesson_data = {
                "lesson_id": item.lesson_id,
                "lesson_type": item.lesson_type,
                "lesson_number": item.lesson_number,
                "lesson_title": item.lesson_title,
                "lesson_desc": item.lesson_desc,
                "lesson_date": item.lesson_date.strftime('%Y-%m-%dT%H:%M:%S.%f'),
                "lesson_end": item.lesson_end
            }
            modules[item.module_id]["module_lessons"].append(lesson_data)

    modules_list = list(modules.values())
    return modules_list
