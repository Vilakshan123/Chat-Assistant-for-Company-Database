def parse_query(user_input):
    # Regex patterns for flexible query parsing
    patterns = {
        r'(show|list|display).*employees.* (.*) department': ('employees_by_dept', 2),
        r'(who is|who\'s|who).*manager.* (.*) department': ('manager_of_dept', 2),
        r'(list|show).*employees hired after (.*)': ('employees_hired_after', 2),
        r'(total|sum).*salary.* (.*) department': ('total_salary_dept', 2)
    }

    user_input = user_input.lower().strip()
    for pattern, (func, group_num) in patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            param = match.group(group_num).strip()
            return func, param
    return None, None