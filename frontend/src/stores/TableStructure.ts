import { ref } from 'vue'

// 研究领域数据（从后端获取）
export const researchFields = ref<Array<{ id: number; research_field: string }>>([])

// 表结构定义
export const tableSchemas = {
  student: [
    {
      name: 'student_id',
      label: '学生学号',
      type: 'text',
      rules: [
        { required: true, message: '学号不能为空' },
        { pattern: /^\d{10}$/, message: '学号必须为10位数字' },
      ],
      primaryKey: true,
    },
    {
      name: 'name',
      label: '姓名',
      type: 'text',
      rules: [{ required: true, message: '姓名不能为空' }],
    },
    {
      name: 'gender',
      label: '性别',
      type: 'select',
      options: [
        { value: '男', label: '男' },
        { value: '女', label: '女' },
      ],
      rules: [{ required: false, message: '请选择性别' }],
    },
    {
      name: 'grade',
      label: '年级',
      type: 'text',
      rules: [{ required: false, message: '年级不能为空' }],
    },
    {
      name: 'major',
      label: '专业',
      type: 'text',
      rules: [{ required: false, message: '专业不能为空' }],
    },
    {
      name: 'class',
      label: '班级',
      type: 'text',
      rules: [{ required: false, message: '班级不能为空' }],
    },
    {
      name: 'research_field',
      label: '研究领域',
      type: 'multiselect',
      options: researchFields,
      valueKey: 'id',
      labelKey: 'research_field',
      rules: [{ required: false, message: '请至少选择一个研究领域' }],
    },
    {
      name: 'phone',
      label: '联系电话',
      type: 'text',
      rules: [
        { required: false, message: '电话不能为空' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式' },
      ],
    },
    {
      name: 'email',
      label: '电子邮箱',
      type: 'text',
      rules: [
        { required: false, message: '邮箱不能为空' },
        { pattern: /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, message: '邮箱格式不正确' },
      ],
    },
  ],
  teacher: [
    {
      name: 'teacher_id',
      label: '教职工号',
      type: 'text',
      rules: [
        { required: true, message: '教师ID不能为空' },
        { pattern: /^T\d{6}$/, message: '格式应为T+6位数字' },
      ],
      primaryKey: true,
    },
    {
      name: 'name',
      label: '姓名',
      type: 'text',
      rules: [{ required: true, message: '姓名不能为空' }],
    },
    {
      name: 'gender',
      label: '性别',
      type: 'select',
      options: [
        { value: '男', label: '男' },
        { value: '女', label: '女' },
      ],
      rules: [{ required: false, message: '请选择性别' }],
    },
    {
      name: 'title',
      label: '职称',
      type: 'text',
      rules: [{ required: false, message: '职称不能为空' }],
    },
    {
      name: 'college',
      label: '所属学院',
      type: 'text',
      rules: [{ required: false, message: '学院不能为空' }],
    },
    {
      name: 'department',
      label: '所属专业',
      type: 'text',
      rules: [{ required: false, message: '系别不能为空' }],
    },
    {
      name: 'research_field',
      label: '研究领域',
      type: 'multiselect',
      options: researchFields,
      valueKey: 'id',
      labelKey: 'research_field',
      rules: [{ required: false, message: '请至少选择一个研究领域' }],
    },
    {
      name: 'phone',
      label: '联系电话',
      type: 'text',
      rules: [
        { required: false, message: '电话不能为空' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式' },
      ],
    },
    {
      name: 'email',
      label: '电子邮箱',
      type: 'text',
      rules: [
        { required: false, message: '邮箱不能为空' },
        { pattern: /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/, message: '邮箱格式不正确' },
      ],
    },
    {
      name: 'office_location',
      label: '办公地点',
      type: 'text',
      rules: [{ required: false, message: '办公室位置不能为空' }],
    },
    {
      name: 'introduction',
      label: '个人简介',
      type: 'textarea',
      rules: [{ required: false, message: '个人简介不能为空' }],
    },
  ],
  project: [
    {
      name: 'project_id',
      label: '项目编号',
      type: 'text',
      rules: [
        { required: true, message: '项目ID不能为空' },
        { pattern: /^P\d{8}$/, message: '格式应为P+8位数字' },
      ],
      primaryKey: true,
    },
    {
      name: 'project_name',
      label: '项目名称',
      type: 'text',
      rules: [{ required: true, message: '项目名称不能为空' }],
    },
    {
      name: 'research_field',
      label: '研究领域',
      type: 'multiselect',
      options: researchFields,
      valueKey: 'id',
      labelKey: 'research_field',
      rules: [{ required: false, message: '请至少选择一个研究领域' }],
    },
    {
      name: 'project_content',
      label: '项目内容',
      type: 'textarea',
      rules: [{ required: false, message: '项目内容不能为空' }],
    },
    {
      name: 'project_application_status',
      label: '申报状态',
      type: 'select',
      options: [
        { value: '未申报', label: '未申报' },
        { value: '申报通过', label: '申报通过' },
      ],
      rules: [{ required: false, message: '请选择申报状态' }],
    },
    {
      name: 'project_approval_status',
      label: '审批状态',
      type: 'select',
      options: [
        { value: '未审批', label: '未审批' },
        { value: '审批通过', label: '审批通过' },
      ],
      rules: [{ required: false, message: '请选择审批状态' }],
    },
    {
      name: 'project_acceptance_status',
      label: '验收状态',
      type: 'select',
      options: [
        { value: '未验收', label: '未验收' },
        { value: '验收通过', label: '验收通过' },
      ],
      rules: [{ required: false, message: '请选择验收状态' }],
    },
  ],
  project_submit: [
    {
      name: 'project_id',
      label: '项目编号',
      type: 'text',
      rules: [
        { required: true, message: '项目ID不能为空' },
        { pattern: /^P\d{8}$/, message: '格式应为P+8位数字' },
      ],
      primaryKey: true,
    },
    {
      name: 'project_name',
      label: '项目名称',
      type: 'text',
      rules: [{ required: true, message: '项目名称不能为空' }],
    },
    {
      name: 'research_field',
      label: '研究领域',
      type: 'multiselect',
      options: researchFields,
      valueKey: 'id',
      labelKey: 'research_field',
      rules: [{ required: false, message: '请至少选择一个研究领域' }],
    },
    {
      name: 'project_content',
      label: '项目内容',
      type: 'textarea',
      rules: [{ required: false, message: '项目内容不能为空' }],
    },
    {
      name: 'head',
      label: '负责人',
      type: 'fixed-user',
      rules: [{ required: false, message: '负责人不能为空' }],
    },
    {
      name: 'members',
      label: '成员',
      type: 'member-select',
      rules: [{ required: false, message: '能为空' }],
    },
    {
      name: 'instructors',
      label: '指导教师',
      type: 'member-select',
      rules: [{ required: false, message: '能为空' }],
    },
  ],
}

// 获取表结构
export function getTableSchema(tableName: 'student' | 'teacher' | 'project' | 'project_submit') {
  return tableSchemas[tableName]
}
// 获取主键字段
export function getPrimaryKey(tableName: 'student' | 'teacher' | 'project' | 'project_submit') {
  const schema = tableSchemas[tableName]
  const primaryKeyField = schema.find((field) => field.primaryKey)
  return primaryKeyField ? primaryKeyField.name : null
}
