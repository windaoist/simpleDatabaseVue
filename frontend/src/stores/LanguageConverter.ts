// 定义中英文映射表
const conceptMap: Record<string, string> = {
  id: '序号',
  research_field: '研究领域',
  project_id: '项目编号',
  project_name: '项目名称',
  project_content: '项目内容',
  leader_names: '负责人',
  member_names: '成员',
  teacher_names: '指导老师',
  project_application_status: '申报状态',
  project_approval_status: '审批状态',
  project_acceptance_status: '验收状态',
  student_id: '学生学号',
  name: '姓名',
  gender: '性别',
  grade: '年级',
  major: '专业',
  class: '班级',
  phone: '联系电话',
  email: '电子邮箱',
  teacher_id: '教职工号',
  title: '职称',
  college: '所属学院',
  department: '所属专业',
  office_location: '办公地点',
  introduction: '个人简介',
}

// 构建英文 -> 中文 Map
const englishToChineseMap = new Map<string, string>(Object.entries(conceptMap))

// 构建中文 -> 英文 Map
const chineseToEnglishMap = new Map<string, string>(
  Object.entries(conceptMap).map(([en, zh]) => [zh, en]),
)

// 英文转中文
export function translateToChinese(english: string): string {
  return englishToChineseMap.get(english) || `未找到对应中文: ${english}`
}

// 中文转英文
export function translateToEnglish(chinese: string): string {
  return chineseToEnglishMap.get(chinese) || `未找到对应英文: ${chinese}`
}
