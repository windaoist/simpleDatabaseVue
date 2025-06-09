// 定义中英文映射表
const conceptMap: Record<string, string> = {
    'id': '序号',
    'project_name': '项目名称',
    'project_status': '项目状态',
    'industry_chain': '所属产业链',
    'project_content': '项目内容',
    'investor': '投资方',
    'investment_amount': '投资额',
    'financing_amount': '融资额',
    'equity_financing': '股权融资',
    'debt_financing': '债权融资',
    'project_progress': '项目进展及资本对接情况',
    'location': '落地区域',
    'contact_person': '联系人',
    'phone': '电话',
    'contact_phone': '联系方式',
    'fund_name': '基金名称',
    'management_agency': '管理机构',
    'investment_area': '投资领域',
    'fundraising_amount': '募资规模',
    'total_investment': '投资总金额',
    'expert_name': '专家',
    'industry_category': '产业类别',
    'specific_industry': '具体产业',
    'agency_name': '机构名称'
};

// 构建英文 -> 中文 Map
const englishToChineseMap = new Map<string, string>(Object.entries(conceptMap));

// 构建中文 -> 英文 Map
const chineseToEnglishMap = new Map<string, string>(
  Object.entries(conceptMap).map(([en, zh]) => [zh, en])
);

// 英文转中文
export function translateToChinese(english: string): string {
  return englishToChineseMap.get(english) || `未找到对应中文: ${english}`;
}

// 中文转英文
export function translateToEnglish(chinese: string): string {
  return chineseToEnglishMap.get(chinese) || `未找到对应英文: ${chinese}`;
}