const studentAttribute: Array<string> = [
  'student_id',
  'name',
  'gender',
  'major',
  'class',
  'research_field',
  'phone',
  'email',
]
const teacherAttribute: Array<string> = [
  'teacher_id',
  'name',
  'gender',
  'title',
  'college',
  'department',
  'research_field',
  'phone',
  'email',
  'office_location',
  'introduction',
]
const projectAttribute: Array<string> = [
  'project_id',
  'project_name',
  'research_field',
  'project_content',
  'project_application_status',
  'project_approval_status',
  'project_acceptance_status',
]
export function getAttribute(table: string) {
  if (table == 'student') {
    return studentAttribute
  } else if (table == 'teacher') {
    return teacherAttribute
  } else if (table == 'project') {
    return projectAttribute
  }
}
